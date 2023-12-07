import argparse
import os
import json
import pandas as pd
from PIL import ImageFont
from utils import utils


def parse_args():
    parser = argparse.ArgumentParser(description='Generate output images')
    parser.add_argument('--data', type=str, default='./data.json', help='input csv file')
    parser.add_argument('--output-dir', type=str, default='output', help='output folder')
    parser.add_argument('--template', type=str, default='template.jpg', help='template image')
    parser.add_argument('--scale', type=float, default=1, help='scale of template image')

    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    # read data file and check its format
    if args.data.endswith('.json'):
        with open(args.data) as f:
            data = json.load(f)

    # create output folder if not exists
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir, exist_ok=True)

    # read list of datas and check its format
    data_list_path = data['path']
    if not os.path.exists(data_list_path):
        raise ValueError(f'Invalid data file path: {data_list_path}')

    if data_list_path.endswith('.csv'):
        df = pd.read_csv(data_list_path)
    elif data_list_path.endswith('.xlsx') or data_list_path.endswith('.xls'):
        df = pd.read_excel(data_list_path)
    else:
        raise ValueError('Invalid input file format (only csv and excel are supported)')

    data_components = data['components']
    assert isinstance(data_components, dict), 'Invalid data components format'

    pipelines = []
    # check if all data components are in the data file
    for component, value in data_components.items():
        assert component in df.columns, f'Invalid data component: {component}'
        if value['type'] == 'text':

            def func(image, text, value=value):
                return utils.draw_text_box(image, text, value['max-width'], value['max-height'], value['x'], value['y'],
                                           ImageFont.truetype(value['font-family'], value['font-size']),
                                           value['font-color'])

            pipelines.append((component, func))

    # read template image
    template = utils.read_template(args.template, args.scale)

    # iterate over data rows
    for index, row in df.iterrows():
        # create a copy of the template image
        img = template.copy()

        # iterate over data components
        for component, pipline in pipelines:
            img = pipline(img, row[component])
        # save the output image
        img.save(os.path.join(args.output_dir, f'{index}.png'))


if __name__ == '__main__':
    main()
