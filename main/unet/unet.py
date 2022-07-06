from typing import List

from keras import Model, Sequential
from keras.layers import Conv2DTranspose, Concatenate
from tensorflow import keras
from tensorflow_examples.models.pix2pix import pix2pix

width = 128
height = 128


def make_unet(output_channels) -> Model:
    base_model = keras.applications.MobileNetV2(input_shape=[128, 128, 3], include_top=False)

    layer_names = [
        'block_1_expand_relu',  # 64x64
        'block_3_expand_relu',  # 32x32
        'block_6_expand_relu',  # 16x16
        'block_13_expand_relu',  # 8x8
        'block_16_project',  # 4x4
    ]
    layers = [base_model.get_layer(name).output for name in layer_names]

    down_stack = keras.Model(inputs=base_model.input, outputs=layers)
    down_stack.trainable = False

    inputs = keras.layers.Input(shape=[128, 128, 3])
    inputs_copy = inputs

    # Downsampling através do modelo
    skips = down_stack(inputs_copy)
    inputs_copy = skips[-1]
    skips = reversed(skips[:-1])

    up_stack: List[Sequential] = [
        pix2pix.upsample(512, 3),  # 4x4 -> 8x8
        pix2pix.upsample(256, 3),  # 8x8 -> 16x16
        pix2pix.upsample(128, 3),  # 16x16 -> 32x32
        pix2pix.upsample(64, 3),  # 32x32 -> 64x64
    ]

    # Upsampling e estabelecimento das conexões de salto
    for up, skip in zip(up_stack, skips):
        inputs_copy = up(inputs_copy)
        concat = Concatenate()
        inputs_copy = concat([inputs_copy, skip])

    # 64x64 -> 128x128
    last = Conv2DTranspose(output_channels, 3, strides=2, padding='same', activation='softmax')
    inputs_copy = last(inputs_copy)
    return keras.Model(inputs=inputs, outputs=inputs_copy)
