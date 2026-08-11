# Gesture Specification

## 1. Gesture Philosophy

Gesture recognition must be stable rather than merely fast.

A gesture should be accepted only when it remains valid for several consecutive frames.

Recommended:

```text
Detection threshold = 3–5 frames
```

## 2. Open Palm

### Detection

All four non-thumb fingers are extended.

### Action

Reset the application.

```text
Filter → Original
Intensity → Default
RGB → Default
```

## 3. Index Finger

### Detection

Index finger extended while other fingers are folded.

### Action

Enter selection/interactions.

## 4. Two Fingers

### Detection

Index + middle fingers extended.

### Action

Move to the next filter.

A cooldown should be used so that one gesture does not skip multiple filters.

Example:

```text
Cooldown = 500 ms
```

## 5. Three Fingers

### Detection

Index + middle + ring fingers extended.

### Action

Enter RGB control mode.

## 6. Pinch

### Detection

Distance between:

```text
Thumb tip
Index tip
```

is below a configurable threshold.

### Action

Control filter intensity.

Normalized distance:

```text
intensity = normalize(distance)
```

Clamp:

```text
0.0 <= intensity <= 1.0
```

## 7. Horizontal Finger Movement

Use index fingertip X coordinate.

```text
X decreases -> decrease value
X increases -> increase value
```

Apply a dead zone to prevent accidental changes.

## 8. Thumb Up

### Action

Confirm the current selection.

This can be used as a locking gesture in later versions.

## 9. Debouncing

Do not react to every frame independently.

Example:

```text
Gesture detected
       ↓
Same gesture for N frames?
       ↓
Yes
       ↓
Execute command
```

This prevents jitter and accidental filter changes.

## 10. Gesture Priority

Recommended priority:

```text
Open Palm
    ↓
Pinch
    ↓
Three Fingers
    ↓
Two Fingers
    ↓
Index
    ↓
None
```

More specific gestures should be evaluated before generic finger states.
