from miniuci import app


def main() -> None:
    config = app.parse_args()
    app.App(config).run()


if __name__ == "__main__":
    main()
