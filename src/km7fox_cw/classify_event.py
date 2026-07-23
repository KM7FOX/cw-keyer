ELEMENT_THRESHOLD_SCALAR = 2.0
WORD_GAP_THRESHOLD_SCALAR = 5.0


def classify_event(event, timing) -> str:
    if event.state == "DOWN":
        return "-" if event.duration_ms > ELEMENT_THRESHOLD_SCALAR * timing.dit_ms else "."

    if event.duration_ms > WORD_GAP_THRESHOLD_SCALAR * timing.dit_ms:
        return "<EOW>"
    elif event.duration_ms > ELEMENT_THRESHOLD_SCALAR * timing.dit_ms:
        return "<EOC>"
    else:
        return ""
    