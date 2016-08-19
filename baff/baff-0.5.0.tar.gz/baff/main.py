from factory import make_api_application, \
                    parse_args, \
                    main_loop, \
                    parse_config, \
                    load_tabs


if __name__ == '__main__':
    try:
        parsed = parse_args()
        config = parse_config(file=parsed.c)
        tabs = load_tabs(config=config)
        main_loop(tabs=tabs, port=4545)
    except KeyboardInterrupt:
        print("bye")