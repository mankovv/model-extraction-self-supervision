from argparse import ArgumentParser

from pytorch_lightning import Trainer
from torch.utils.data import DataLoader
from torchvision.transforms import CenterCrop, Compose, Normalize, Resize, ToTensor

from dataset import ImageNetWithLogits
from model import ImageNetClassifier

MEAN = [0.485, 0.456, 0.406]
STD = [0.229, 0.224, 0.225]


def main():
    parser = ArgumentParser(description="ImageNet Testing", allow_abbrev=False)
    parser.add_argument(
        "--data-dir", type=str, default="data", help="ImageNet data directory."
    )
    parser.add_argument(
        "--logits-file",
        type=str,
        required=False,
        help="Extracted target logits file path.",
    )
    parser.add_argument(
        "--chkpt", type=str, required=True, help="Finetuned model checkpoint."
    )
    parser.add_argument("--batch-size", type=int, default=256)
    parser.add_argument("--num-workers", type=int, default=32)

    parser = Trainer.add_argparse_args(parser)

    args = parser.parse_args()

    model = ImageNetClassifier.load_from_checkpoint(args.chkpt)

    transform = Compose(
        [Resize(256), CenterCrop(224), ToTensor(), Normalize(mean=MEAN, std=STD)]
    )
    test_data = ImageNetWithLogits(
        root=args.data_dir,
        logits_file=args.logits_file,
        split="test",
        meta_dir=args.data_dir,
        transform=transform,
    )
    test_dataloader = DataLoader(
        test_data,
        batch_size=args.batch_size,
        num_workers=args.num_workers,
        shuffle=False,
    )

    trainer = Trainer.from_argparse_args(args)
    trainer.test(model, test_dataloader)


if __name__ == "__main__":
    main()
