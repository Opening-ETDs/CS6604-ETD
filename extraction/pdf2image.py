
import os, shutil, subprocess, glob, argparse


def render_pdf(pdf_path, pdf_name, output_image_folder, output_image_format, dpi):
    print("Processing: ", pdf_path)

    output_image_folder = os.path.join(output_image_folder, pdf_name.split('.pdf')[0])

    if os.path.exists(output_image_folder):
        shutil.rmtree(output_image_folder)
    os.makedirs(output_image_folder)

    image_output_path_template = output_image_folder + '/' + '%04d.{ext}'.format(ext=output_image_format)
    sdevice = 'png16m' if output_image_format == 'png' else 'jpeg'

    gs_args = [
        'gs', '-dGraphicsAlphaBits=4', '-dTextAlphaBits=4', '-dNOPAUSE', '-dBATCH', '-dSAFER', '-dQUIET',
        '-sDEVICE=' + sdevice,
        '-r%d' % dpi, '-sOutputFile=' + image_output_path_template,
        '-dBufferSpace=%d' % int(1e9),
        '-dBandBufferSpace=%d' % int(5e8), '-sBandListStorage=memory',
        '-c',
        '%d setvmthreshold' % int(1e9), '-dNOGC',
        '-dNumRenderingThreads=4', "-f", pdf_path
    ]

    print('Running command: ', ' '.join(gs_args))
    subprocess.run(gs_args)


def run_bulk(input_pdf_folder, output_image_folder):
    '''
    Invokes the render() function in a loop for each PDF in pdf_folder.
    :param input_pdf_folder: The path to the folder containing the pdfs that need to be converted to images.
    :param output_image_folder: the path to the folder where rendered pdfs should be stored.
    :return: None
    '''
    input_pdf_folder = os.path.abspath(input_pdf_folder)
    output_image_folder = os.path.abspath(output_image_folder)
    pdf_file_paths = glob.glob(os.path.join(input_pdf_folder, '*.pdf'))

    for pdf_file_path in pdf_file_paths:
        render_pdf(pdf_path=pdf_file_path,
                   pdf_name=pdf_file_path.split('/')[-1],
                   output_image_folder=output_image_folder,
                   output_image_format='png',
                   dpi=100)


def run_single(input_pdf_path, output_image_folder):
    '''
    Invokes the render() function for a single input PDF.
    '''
    input_pdf_path = os.path.abspath(input_pdf_path)
    output_image_folder = os.path.abspath(output_image_folder)

    render_pdf(pdf_path=input_pdf_path,
            pdf_name=input_pdf_path.split('/')[-1],
            output_image_folder=output_image_folder,
            output_image_format='png',
            dpi=100)



if __name__ == "__main__":
    '''
    Converts all the PDFs in pdf_folder into images.
    '''
    parser = argparse.ArgumentParser(description='Converts one or multiple PDFs to images. Needs ghostscript to be installes on the host system.')
    parser.add_argument("--input", help="This can either be the path to a single PDF or a directory containing one or more PDFs.")
    parser.add_argument("--output", help="This always needs to be a directory. "
                                         "If this directory does not exist, an attempt will be made to create it. "
                                         "For each input PDF, a directory will be created and the images for each page will be written to this directory.")
    args = parser.parse_args()

    if os.path.isfile(os.path.abspath(args.input)):
        print('Running for a single PDF.')
        run_single(args.input, args.output)
    elif os.path.isdir(os.path.abspath(args.input)):
        print('Running for a directory.')
        run_bulk(args.input, args.output)
    else:
        print('Input seems invalid.')

