import os
import json
from dataclasses import dataclass, field


@dataclass
class UsedLanguages:
    lang_stats: dict[str, int] = field(init=False, default_factory=dict)
    lang_sum: int = field(init=False, default=0)
    excluded_lang: list[str] = field(init=False)
    lang_name_map: dict[str, str] = field(init=False)

    def __post_init__(self):
        try:
            self.excluded_lang = json.loads(
                UsedLanguages.__get_env_value("LANG_TO_EXCLUDE")
            )
        except:
            raise Exception(
                "Value of LANG_TO_EXCLUDE is not valid JSON structure"
            )

        try:
            self.lang_name_map = json.loads(
                UsedLanguages.__get_env_value("LANG_NAME_MAP")
            )
        except:
            raise Exception(
                "Value of LANG_NAME_MAP is not valid JSON structure"
            )

    def add(self, repo_language: dict[str, int]):
        for language, value in repo_language.items():
            if language not in self.excluded_lang:
                lang_name = self.lang_name_map.get(language, language)
                self.lang_stats[lang_name] = (
                    self.lang_stats.get(lang_name, 0) + value
                )
                self.lang_sum = self.lang_sum + value

    def get_percentage_summary(self):
        return {
            k: round(((v/self.lang_sum)), 4)
            for k, v in sorted(self.lang_stats.items(), key=lambda item: item[1])
        }

    @staticmethod
    def __get_env_value(env_name: str):
        value = os.getenv(env_name, None)
        if value is not None:
            return value

        raise Exception(
            "Cannot find environmental variable: {env_var_name}".format(
                env_var_name=env_name
            )
        )
