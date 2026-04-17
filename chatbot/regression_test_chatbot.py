import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from chatbot import CustomChatbot


def run_regression():
    website_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    bot = CustomChatbot(website_root)

    cases = [
        {
            'name': 'Natural language date with ordinal',
            'query': 'show events on January 26th',
            'expect_any': ['Events on 2026-01-26']
        },
        {
            'name': 'Natural language date variant',
            'query': 'events on January 24th',
            'expect_any': ['Events on 2026-01-24']
        },
        {
            'name': 'Email extraction reliability',
            'query': 'what is your email',
            'expect_any': ['milehighmovement@gmail.com']
        },
        {
            'name': 'Activity precision: basketball',
            'query': 'tell me about basketball',
            'expect_any': ['BASKETBALL']
        },
        {
            'name': 'Activity precision: pickleball',
            'query': 'do you have pickleball',
            'expect_any': ['PICKLEBALL']
        },
        {
            'name': 'Follow-up memory: tomorrow',
            'query': 'what about tomorrow?',
            'expect_any': ['Events on 2026-01-25']
        },
        {
            'name': 'Follow-up memory: same day next month',
            'query': 'same day next month',
            'expect_any': ['Events on 2026-02-25', 'Events on 2026-02-24', 'Events on 2026-02-26']
        },
        {
            'name': 'Follow-up memory: that date kids filter',
            'query': 'that date for kids activities',
            'expect_any': ['Youth', 'Kids', 'Family', 'I do not see events listed for']
        }
    ]

    # Prime context for follow-up checks.
    bot.ask('events on January 24th')

    failures = []
    for case in cases:
        response = bot.ask(case['query'])
        passed = any(expected in response for expected in case['expect_any'])
        if not passed:
            failures.append((case['name'], case['query'], response))
        status = 'PASS' if passed else 'FAIL'
        print(f"[{status}] {case['name']}: {case['query']}")
        print(response)
        print('-' * 80)

    if failures:
        print('Regression failures:')
        for name, query, response in failures:
            print(f"- {name} | query={query} | response={response}")
        raise SystemExit(1)

    print('All regression checks passed.')


if __name__ == '__main__':
    run_regression()
