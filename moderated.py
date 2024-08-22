import json
from openai import OpenAI
from colorama import Fore, Back, Style, init

init(autoreset=True)

client = OpenAI(
    api_key=''
)

print(f"{Style.RESET_ALL}")
text2mod=input(">")
moderation = client.moderations.create(input=text2mod)

def create_bar(score):
    bar_length = int(score * 20)
    bar = f"{Style.RESET_ALL}[{Fore.YELLOW}{'#' * bar_length}{' ' * (20 - bar_length)}{Style.RESET_ALL}] {Fore.YELLOW}{score:.2f}{Style.RESET_ALL}"
    return bar

def format_flagged_text(value):
    if value:
        return f"{Back.GREEN}True{Style.RESET_ALL}"
    else:
        return f"{Back.RED}False{Style.RESET_ALL}"

def format_line(label, content, width=25):
    return f"{label.ljust(width)}: {content}"

response = {
    "id": moderation.id,
    "model": moderation.model,
    "results": []
}

for result in moderation.results:
    formatted_result = {
        "flagged": format_flagged_text(result.flagged),
        "categories": {
            "harassment": format_flagged_text(result.categories.harassment),
            "harassment_threatening": format_flagged_text(result.categories.harassment_threatening),
            "hate": format_flagged_text(result.categories.hate),
            "hate_threatening": format_flagged_text(result.categories.hate_threatening),
            "self_harm": format_flagged_text(result.categories.self_harm),
            "self_harm_instructions": format_flagged_text(result.categories.self_harm_instructions),
            "self_harm_intent": format_flagged_text(result.categories.self_harm_intent),
            "sexual": format_flagged_text(result.categories.sexual),
            "sexual_minors": format_flagged_text(result.categories.sexual_minors),
            "violence": format_flagged_text(result.categories.violence),
            "violence_graphic": format_flagged_text(result.categories.violence_graphic)
        },
        "category_scores": {
            "harassment": create_bar(result.category_scores.harassment),
            "harassment_threatening": create_bar(result.category_scores.harassment_threatening),
            "hate": create_bar(result.category_scores.hate),
            "hate_threatening": create_bar(result.category_scores.hate_threatening),
            "self_harm": create_bar(result.category_scores.self_harm),
            "self_harm_instructions": create_bar(result.category_scores.self_harm_instructions),
            "self_harm_intent": create_bar(result.category_scores.self_harm_intent),
            "sexual": create_bar(result.category_scores.sexual),
            "sexual_minors": create_bar(result.category_scores.sexual_minors),
            "violence": create_bar(result.category_scores.violence),
            "violence_graphic": create_bar(result.category_scores.violence_graphic)
        }
    }
    response["results"].append(formatted_result)

for result in response["results"]:
    print(format_line("Flagged", result['flagged']))
    print("\nCategories:")
    for category, flagged in result["categories"].items():
        print(format_line(category, flagged))
    print("\nCategory Scores:")
    for score, bar in result["category_scores"].items():
        print(format_line(score, bar))
    print("\n")
