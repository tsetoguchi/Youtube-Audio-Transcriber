## Disclaimer
YouTube videos with more complex sources of audio i.e., music with heavy spectral content may not be accurately transcribed.


# Quick Start

## Adding YouTube videos

To add YouTube videos, add links to the `urls` list in `main.py`.

```
    urls = [
        "https://www.youtube.com/watch?v=KNtJGQkC-WI&ab_channel=ArianaGrandeVevo",
        "https://www.youtube.com/watch?v=Z-48u_uWMHY&ab_channel=KendrickLamarVEVO"  # Add more URLs as needed
    ]
```



## Changing the quality of the transcription

If the transcription is inaccurate, and time efficiency is a non-issue, it may help to change the `whisper` model used in `main.py`. Larger models also require more powerful hardware.

Options include:
`base` `small` `medium` `large`

```
    model = whisper.load_model("large")
```
