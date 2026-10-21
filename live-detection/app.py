
from flask import Flask, render_template_string

app = Flask(__name__)

PAGE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<title>Termux CV | Live Detection</title>
<style>
:root { color-scheme: dark; }
* { box-sizing: border-box; }
body {
  margin: 0; padding: 14px; background: #101318; color: #f3f5f7;
  font-family: system-ui, sans-serif;
}
main { max-width: 900px; margin: auto; }
h2 { margin: 4px 0; font-size: 1.35rem; }
.sub { color: #aab4c0; font-size: .9rem; margin-bottom: 14px; }
.stage {
  position: relative; width: 100%; overflow: hidden;
  background: #050607; border-radius: 14px; min-height: 180px;
}
video { display: block; width: 100%; height: auto; }
canvas#overlay { position: absolute; inset: 0; width: 100%; height: 100%; pointer-events: none; }
.panel {
  margin-top: 12px; padding: 14px; background: #1a2029;
  border: 1px solid #2b3441; border-radius: 12px;
}
.status { font-size: .9rem; color: #a9e8c1; min-height: 1.4em; }
.stats { display: grid; grid-template-columns: repeat(3,1fr); gap: 8px; margin-top: 10px; }
.stat { background: #10151c; border-radius: 8px; padding: 10px; min-width: 0; }
.stat small { color: #aab4c0; display: block; }
.stat strong { font-size: 1.05rem; overflow-wrap: anywhere; }
.controls { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; }
button {
  border: 0; border-radius: 9px; padding: 11px 14px;
  background: #d7e7ff; color: #101820; font-weight: 650; font-size: .92rem;
}
button.secondary { background: #303a48; color: #f3f5f7; }
label { display: block; font-size: .9rem; margin: 13px 0 5px; }
input[type=range] { width: 100%; }
select {
  width: 100%; background: #10151c; color: white; padding: 10px;
  border: 1px solid #394555; border-radius: 8px;
}
#objects { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 10px; }
.tag { background: #263546; padding: 6px 9px; border-radius: 7px; font-size: .82rem; }
.note { color: #aab4c0; font-size: .82rem; line-height: 1.5; }
@media(max-width:480px) {
  body { padding: 9px; }
  .stats { grid-template-columns: repeat(3,minmax(0,1fr)); }
  .stat { padding: 8px 5px; }
  .stat strong { font-size: .92rem; }
}
</style>
</head>
<body>
<main>
  <h2>📷 Live Object Detection v2</h2>
  <div class="sub">Browser-based AI · Termux Flask server · COCO-SSD</div>

  <div class="stage">
    <video id="video" autoplay playsinline muted></video>
    <canvas id="overlay"></canvas>
  </div>

  <section class="panel">
    <div id="status" class="status">Loading TensorFlow.js…</div>
    <div class="stats">
      <div class="stat"><small>AI FPS</small><strong id="fps">—</strong></div>
      <div class="stat"><small>Inference</small><strong id="latency">—</strong></div>
      <div class="stat"><small>Camera</small><strong id="resolution">—</strong></div>
    </div>

    <label for="confidence">Confidence threshold: <span id="confValue">35%</span></label>
    <input id="confidence" type="range" min="10" max="80" value="35">

    <label for="interval">Detection speed</label>
    <select id="interval">
      <option value="0">Fastest practical</option>
      <option value="100" selected>Balanced</option>
      <option value="220">Lower CPU usage</option>
    </select>

    <label for="inferenceWidth">AI input resolution</label>
    <select id="inferenceWidth">
      <option value="416">416 px — lighter</option>
      <option value="640" selected>640 px — balanced</option>
      <option value="800">800 px — more detail, slower</option>
    </select>

    <div class="controls">
      <button id="pauseBtn">Pause AI</button>
      <button id="cameraBtn" class="secondary">Switch camera</button>
      <button id="restartBtn" class="secondary">Restart camera</button>
    </div>
    <div id="objects"></div>
    <p class="note">
      This model recognizes predefined COCO classes. Lower confidence may reveal
      weaker predictions but can also increase false detections. AI input size
      affects speed and detail; it does not add new classes.
    </p>
  </section>
</main>

<canvas id="inferenceCanvas" hidden></canvas>

<script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@4.22.0/dist/tf.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@tensorflow-models/coco-ssd@2.2.3/dist/coco-ssd.min.js"></script>
<script>
const video = document.getElementById('video');
const overlay = document.getElementById('overlay');
const ctx = overlay.getContext('2d');
const inferCanvas = document.getElementById('inferenceCanvas');
const inferCtx = inferCanvas.getContext('2d', { willReadFrequently: true });
const statusEl = document.getElementById('status');
const objectsEl = document.getElementById('objects');

let model = null;
let stream = null;
let busy = false;
let paused = false;
let facing = 'environment';
let lastInference = 0;
let frames = 0;
let fpsStart = performance.now();
let currentPredictions = [];

function setStatus(message, error = false) {
  statusEl.textContent = message;
  statusEl.style.color = error ? '#ff9d9d' : '#a9e8c1';
}

async function startCamera() {
  stopCameraTracks();
  setStatus('Requesting camera permission…');

  try {
    stream = await navigator.mediaDevices.getUserMedia({
      audio: false,
      video: {
        facingMode: { ideal: facing },
        width: { ideal: 1280 },
        height: { ideal: 720 },
        frameRate: { ideal: 30, max: 30 }
      }
    });
    video.srcObject = stream;
    await video.play();

    overlay.width = video.videoWidth;
    overlay.height = video.videoHeight;
    document.getElementById('resolution').textContent =
      video.videoWidth + '×' + video.videoHeight;
    setStatus('Camera ready. Starting AI…');
  } catch (e) {
    setStatus('Camera error: ' + e.message +
      '. Allow camera permission and open http://127.0.0.1:5000', true);
  }
}

function stopCameraTracks() {
  if (stream) stream.getTracks().forEach(track => track.stop());
  stream = null;
  video.srcObject = null;
}

async function loadModel() {
  try {
    if (!window.tf || !window.cocoSsd) {
      throw new Error('AI scripts did not load. Check internet and reload.');
    }
    setStatus('Preparing WebGL backend…');
    try {
      await tf.setBackend('webgl');
    } catch (_) {
      await tf.setBackend('cpu');
    }
    await tf.ready();

    setStatus('Downloading COCO-SSD MobileNet V2 model…');
    model = await cocoSsd.load({ base: 'mobilenet_v2' });
    setStatus('Model ready. Point the camera at objects.');
    detectLoop();
  } catch (e) {
    setStatus('Model failed: ' + e.message + '. Reload with internet access.', true);
  }
}

function drawBoxes(predictions) {
  if (!video.videoWidth || !video.videoHeight) return;
  if (overlay.width !== video.videoWidth || overlay.height !== video.videoHeight) {
    overlay.width = video.videoWidth;
    overlay.height = video.videoHeight;
  }

  ctx.clearRect(0, 0, overlay.width, overlay.height);
  const sx = overlay.width / inferCanvas.width;
  const sy = overlay.height / inferCanvas.height;
  const threshold = Number(document.getElementById('confidence').value) / 100;

  for (const p of predictions) {
    if (p.score < threshold) continue;
    const [x, y, w, h] = p.bbox;
    const bx = x * sx, by = y * sy, bw = w * sx, bh = h * sy;
    const label = p.class + ' ' + Math.round(p.score * 100) + '%';
    const fontSize = Math.max(14, Math.round(overlay.width / 55));

    ctx.lineWidth = Math.max(2, overlay.width / 450);
    ctx.strokeStyle = '#43ff83';
    ctx.strokeRect(bx, by, bw, bh);
    ctx.font = 'bold ' + fontSize + 'px system-ui, sans-serif';
    const textWidth = ctx.measureText(label).width;
    const labelHeight = fontSize + 8;
    const labelY = Math.max(labelHeight, by);

    ctx.fillStyle = '#43ff83';
    ctx.fillRect(bx, labelY - labelHeight, textWidth + 12, labelHeight);
    ctx.fillStyle = '#06120a';
    ctx.fillText(label, bx + 6, labelY - 5);
  }
}

function updateObjectList(predictions) {
  const threshold = Number(document.getElementById('confidence').value) / 100;
  const counts = {};
  for (const p of predictions) {
    if (p.score >= threshold) counts[p.class] = (counts[p.class] || 0) + 1;
  }
  const names = Object.entries(counts).sort((a,b) => b[1] - a[1]);
  objectsEl.replaceChildren();

  if (!names.length) {
    const span = document.createElement('span');
    span.className = 'note';
    span.textContent = 'No objects above the current confidence threshold.';
    objectsEl.appendChild(span);
    return;
  }

  for (const [name, count] of names) {
    const span = document.createElement('span');
    span.className = 'tag';
    span.textContent = name + (count > 1 ? ' ×' + count : '');
    objectsEl.appendChild(span);
  }
}

async function detectLoop() {
  if (!model) return;

  if (!paused && video.readyState >= 2 && !busy) {
    const now = performance.now();
    const interval = Number(document.getElementById('interval').value);
    if (now - lastInference >= interval) {
      busy = true;
      lastInference = now;
      try {
        const targetWidth = Number(document.getElementById('inferenceWidth').value);
        const ratio = video.videoHeight / video.videoWidth;
        inferCanvas.width = targetWidth;
        inferCanvas.height = Math.max(1, Math.round(targetWidth * ratio));
        inferCtx.drawImage(video, 0, 0, inferCanvas.width, inferCanvas.height);

        const start = performance.now();
        const minScore = Number(document.getElementById('confidence').value) / 100;
        currentPredictions = await model.detect(inferCanvas, 30, minScore);
        const elapsed = performance.now() - start;

        drawBoxes(currentPredictions);
        updateObjectList(currentPredictions);
        document.getElementById('latency').textContent = Math.round(elapsed) + ' ms';

        frames++;
        const t = performance.now();
        if (t - fpsStart >= 1000) {
          document.getElementById('fps').textContent =
            (frames * 1000 / (t - fpsStart)).toFixed(1);
          frames = 0;
          fpsStart = t;
        }
      } catch (e) {
        setStatus('Detection error: ' + e.message, true);
      } finally {
        busy = false;
      }
    }
  }

  requestAnimationFrame(detectLoop);
}

document.getElementById('pauseBtn').addEventListener('click', () => {
  paused = !paused;
  document.getElementById('pauseBtn').textContent = paused ? 'Resume AI' : 'Pause AI';
  if (paused) {
    ctx.clearRect(0, 0, overlay.width, overlay.height);
    setStatus('AI paused. Camera is still running.');
  } else {
    setStatus('AI resumed.');
  }
});

document.getElementById('cameraBtn').addEventListener('click', async () => {
  facing = facing === 'environment' ? 'user' : 'environment';
  await startCamera();
});

document.getElementById('restartBtn').addEventListener('click', startCamera);

document.getElementById('confidence').addEventListener('input', e => {
  document.getElementById('confValue').textContent = e.target.value + '%';
});

window.addEventListener('beforeunload', stopCameraTracks);

(async () => {
  await startCamera();
  await loadModel();
})();
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(PAGE)

if __name__ == "__main__":
    print("Live Object Detection v2")
    print("Open http://127.0.0.1:5000 in your phone browser")
    app.run(host="127.0.0.1", port=5000, debug=False, threaded=True)

