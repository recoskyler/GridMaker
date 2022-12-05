# GridMaker

<a href='https://ko-fi.com/recoskyler' target='_blank'><img height='35' style='border:0px;height:46px;' src='https://az743702.vo.msecnd.net/cdn/kofi3.png?v=0' border='0' alt='Buy Me a Coffee at ko-fi.com' />

A simple python script to turn URLs of images to a stitched grid.

## Usage

1. Create a JSON file/list in the following format:

    ```json
    [
        "https://url0.xyz/image0",
        "https://url1.xyz/image1",
        ...
    ]
    ```

2. Run the program:

    ```bash
    $ python gridmaker.py
    ```

3. Enter the required values (if you are not using parameters):

    ```
    === GridMaker 1.0 ===
    Location of the JSON list:  list.json
    Output file path (with the name of the file): grid.jpg
    Width of a single grid item (min 10): 100
    Height of a single grid item (min 10): 100
    Horizontal size of the grid image (min 2): 16
    Vertical size of the grid image (min 2): 9
    ```
