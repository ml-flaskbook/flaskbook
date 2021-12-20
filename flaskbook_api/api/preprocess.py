import torchvision


def image_to_tensor(image):
    """画像データをテンソル型の数値データへ変換"""
    image_tensor = torchvision.transforms.functional.to_tensor(image)
    return image_tensor
