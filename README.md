# Adding YouTube videos

To add YouTube videos, add links to the `urls` list in main.py.

```
    urls = [
        "https://www.youtube.com/watch?v=KNtJGQkC-WI&ab_channel=ArianaGrandeVevo",
        "https://www.youtube.com/watch?v=Z-48u_uWMHY&ab_channel=KendrickLamarVEVO"  # Add more URLs as needed
    ]
```



# Changing the quality of the transcription

If the transcription is not accurate, it may help to change the model used in main.py.
Options include:
`base` `small` `medium` `large`

```
    model = whisper.load_model("large")
```
