import config
from furtherpy.sample import date_conv_tool
from email_reader_repo.sample import email_tool
import get_wiki
from spotify_controller_repo.sample import gsheets_tool
import time
import requests
from bs4 import BeautifulSoup

# Do:
# make it so you can schedule an article!
# add option to save favorites
# option to see backlog -get emailed?


def get_todays_random_wiki():
    # Gets title
    wiki_title = get_wiki.get_random_wiki_title()

    # Gets link
    wiki_link = get_wiki.convert_title_to_link(wiki_title)

    return [wiki_title, wiki_link]


def test_for_bad_title(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find("title")
    title = str(title)[7:]
    title = title[:len(title) - 20]

    # checks if link produces a bad title:
    if title == "Bad title":
        return "bad"
    else:
        return "good"


# Tests to see if wiki link is broken or if there is an error sending the email
def test_wiki_link(wiki_info):
    print("[send_wiki] Testing article link...")

    wiki_title = wiki_info[0]
    wiki_link = wiki_info[1]

    subject = "WIKI LINK TEST for " + wiki_title

    subject_fixed = email_tool.fix_text_format_for_email(subject)

    email_text = "TEST\n\n" + wiki_link[8:]

    # sets default (article is fine)
    result = 1

    try:
        email_tool.send_email(config.test_email_address, config.test_email_password, config.test_email_address,
                             subject_fixed, email_text)
    except UnicodeEncodeError:
        # sets result to show error
        result = 2
    if test_for_bad_title(wiki_link) == "bad":
        # sets result to show error
        result = 3

    return result


def get_email_list():
    service = gsheets_tool.authenticate_sheets_api()
    current_sheet_id = config.email_send_list_google_sheet_id

    raw_email_list = gsheets_tool.get_all_sheets_data(service, current_sheet_id, "A:A")

    email_list = [val for sublist in raw_email_list for val in sublist]

    return email_list


def send_wiki_link(wiki_info):
    wiki_title = wiki_info[0]
    wiki_link = wiki_info[1]

    # Formats email text
    email_text = "Your random Wikipedia article for today!\n\n" + wiki_link[8:]
    subject = "Wiki of the Day: " + wiki_title + " - " + date_conv_tool.get_readable("day")

    subject_fixed = email_tool.fix_text_format_for_email(subject)

    # Gets the wiki-a-day email list
    mailing_list = get_email_list()

    # Sends email to every address on list
    for send_address in mailing_list:
        email_tool.send_email(config.send_wiki_email_address, config.send_wiki_email_password, send_address,
                             subject_fixed, email_text)

    print("[send_wiki] Sent today's random Wiki: " + wiki_title)


# adds email to email list Google Sheet
def add_email_to_list(new_email_address):
    service = gsheets_tool.authenticate_sheets_api()
    current_sheet_id = config.email_send_list_google_sheet_id

    # currently not set up, but has the ability to add name to list
    gsheets_tool.write_data_pair_to_sheet(service, current_sheet_id, "A:B", new_email_address, "")

    email_tool.send_email(config.send_wiki_email_address, config.send_wiki_email_password, new_email_address,
                         "Success! - Wiki of the Day", "You have been successfully added to the Wiki of the Day!")

    print("[send_wiki] Added " + new_email_address + " to email list")


def main():
    # Testing:
    # example that produces bad title:
    # todays_wiki_info = ["causes bad title", "https://en.wikipedia.org/wiki/50/50_&amp;_Lullaby"]

    # example that produces and issue sending as an email:
    # todays_wiki_info = ["causes unicode encode error", "https://en.wikipedia.org/wiki/–"]

    # Gets random article and sends it
    todays_wiki_info = get_todays_random_wiki()

    test_result = test_wiki_link(todays_wiki_info)

    # Sends wiki if link works
    if test_result == 1:
        print("[send_wiki] This article works.")
        send_wiki_link(todays_wiki_info)
        return

    # Tries a new wiki if link fails
    elif test_result == 2:
        print("[send_wiki] There was an issue sending this article as an email. Trying a new one...")

        # pauses before trying again
        time.sleep(2)

        main()
        return
    elif test_result == 3:
        print("[send_wiki] This link produced a bad title. Trying a new one...")

        # pauses before trying again
        time.sleep(2)

        main()
        return


if __name__ == '__main__':
    main()
