import pytest
from utils import utils
from PIL import Image
from PIL import ImageFont


@pytest.fixture
def mock_img(mocker):
    img_size = (256, 128)
    mocker.patch('PIL.Image.open', return_value=Image.new('RGB', img_size, (0, 0, 0)))
    return img_size


def test_read_template(mock_img):
    img_size = mock_img
    scales = [1, .5, 3, 2.1]

    for scale in scales:
        img = utils.read_template('test.jpg', scale)
        assert img.size == (int(img_size[0] * scale), int(img_size[1] * scale))

    with pytest.raises(ValueError):
        utils.read_template('test.jpg', 0)


def test_extract_words():
    input_string = 'This is a test string'
    expected = ['This', 'is', 'a', 'test', 'string']
    assert utils.extract_words(input_string) == expected


def test_draw_text():
    img = Image.new('RGB', (500, 500), (0, 0, 0))
    text = 'One line text'
    x, y = 250, 250
    for i in range(1, 200):
        font = ImageFont.truetype('arial.ttf', i)
        color = (255, 255, 255)
        img = utils.draw_centered_text(img, text, x, y, font, color)

        # finde the Min and Max x and y values for the text
        min_x, min_y, max_x, max_y = img.getbbox()
        assert x - 2 <= (min_x + max_x) / 2 <= x + 2
        assert y - 2 <= (min_y + max_y) / 2 <= y + 2


def test_extract_lines_text():
    txt = 'This is a test string'
    max_chrs = 5
    expected = ['This', 'is a', 'test', 'string']
    assert utils.extract_lines_text(txt, max_chrs) == expected


def test_draw_text_box():
    img = Image.new('RGB', (1000, 1000), (0, 0, 0))
    text = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec a diam lectus. Sed sit amet ipsum mauris. ' \
           'Maecenas congue ligula ac quam viverra nec consectetur ante hendrerit.'
    max_width, max_high = 300, 300
    x, y = 500, 500
    font = ImageFont.truetype('arial.ttf', 16)
    color = (255, 255, 255)
    img = utils.draw_text_box(img, text, max_width, max_high, x, y, font, color)

    # finde the Min and Max x and y values for the text
    min_x, min_y, max_x, max_y = img.getbbox()
    assert x - 2 <= (min_x + max_x) / 2 <= x + 2
    assert y - 2 <= (min_y + max_y) / 2 <= y + 2
    assert max_y - min_y <= max_high
    assert max_x - min_x <= max_width
