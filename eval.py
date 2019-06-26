import collazione.evaluation as eval

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('gt_path', help="unix path")
    parser.add_argument('out_path', help="unix path")
    parser.add_argument('--type', action='store_true')
    args = parser.parse_args()

    eval.listEvaluation(args.gt_path, args.out_path)
