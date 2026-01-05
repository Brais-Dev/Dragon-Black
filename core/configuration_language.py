# File that allows language translation
import os
import json
from pathlib import Path
import configparser


class Translator:
    def __init__(self):
        # Load JSON file that contains the language dictionary
        self.dir_translation = Path(__file__).parent.parent / "data"
        self.translations = self.dir_translation / "file_translation.json"
        self.file_conf = Path(__file__).parent.parent / "core"
        self.file = self.file_conf / "language.conf"
        self.lang = 'en'
        self.current_lang = self.load_language()
        self.strings = self.load_strings(self.current_lang)

    def load_language(self):
        config = configparser.ConfigParser()
        if os.path.exists(self.file):
            config.read(self.file)
            return config.get('LANGUAGE', 'selected', fallback='en')

        else:
            while True:
                print("\u001b[0;33mselect a language")
                print("1 English")
                print("2 Spanish")
                choice = input("\u001b[0;34mselect an option: ")

                if choice in ['1', 'en']:
                    self.lang = 'en'
                    break
                elif choice in ['2', 'es']:
                    self.lang = 'es'
                    break
                else:
                    print("invalid")
            config['LANGUAGE'] = {'selected': self.lang}
            with open(self.file, 'w') as f:
                config.write(f)
            return self.lang

    def load_strings(self, language):
        if os.path.exists(self.translations):
            with open(self.translations, 'r', encoding='utf-8') as f:
                translation = json.load(f)
                string = translation
                return string.get(language, string['en'])

    def t(self, key):
        """Translate a key to the current language"""
        return self.strings.get(key, key)

    def get_error_message(self, error_type, *args):
        """Get formatted error message based on error type"""
        if error_type == "command_rejected":
            base_msg = self.t("error_command_rejected")
            if args:
                return f"{base_msg} {args[0]}"
            return base_msg
        elif error_type == "invalid_command":
            return self.t("error_invalid_command")
        elif error_type == "package_not_found":
            base_msg = self.t("error_package_not_found")
            if args:
                return f"{base_msg} {args[0]}"
            return base_msg
        elif error_type == "already_installed":
            base_msg = self.t("error_already_installed")
            if args:
                return f"{args[0]} {base_msg}"
            return base_msg
        elif error_type == "not_installed":
            base_msg = self.t("error_not_installed")
            if args:
                return f"{args[0]} {base_msg}"
            return base_msg
        elif error_type == "success_installed":
            base_msg = self.t("success_installed")
            if args:
                return f"{args[0]} {base_msg}"
            return base_msg
        elif error_type == "success_uninstalled":
            base_msg = self.t("success_uninstalled")
            if args:
                return f"{args[0]} {base_msg}"
            return base_msg
        elif error_type == "no_results":
            base_msg = self.t("no_results")
            if args:
                return f"{base_msg} '{args[0]}'"
            return base_msg
        elif error_type == "search_results":
            base_msg = self.t("search_results")
            if args:
                return f"{args[0]} {base_msg} '{args[1]}'"
            return base_msg
        else:
            return self.t(error_type)

    def get_info_message(self, info_type, *args):
        """Get formatted info message based on info type"""
        if info_type == "package_info":
            return self.t("package_info")
        elif info_type == "package_installed":
            return self.t("package_installed")
        elif info_type == "package_not_installed":
            return self.t("package_not_installed")
        elif info_type == "available_packages":
            return self.t("available_packages")
        elif info_type == "installed_packages":
            return self.t("installed_packages")
        else:
            return self.t(info_type)


app = Translator()
