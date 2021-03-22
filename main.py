from gui_modules import RootWindow, LoginFrame


def main():
    """
    This function is the entry point of this program.

    Args:
        None

    Returns:
        None
    """
    # Running root window with intital LoginFrame
    RootWindow(LoginFrame, "PyStock | Login").run()


if __name__ == "__main__":
    # Run this only if this file is executed directly.
    main()
