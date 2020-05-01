from wiki_of_the_day_repo.sample import send_wiki
from furtherpy.sample import files_tool
import time


print("\n[forever_send_wiki] Starting send_wiki.py")
while 1:
    try:
        send_wiki.main()

    except Exception as e:
        # saves error file
        files_tool.basic_write_file("forever_send_wiki_crash_report", "send_wiki crashed with the exception: " + str(e))

        print("\n[forever_send_wiki] The error: '" + str(e) +
              "' occurred while running send_wiki.py.\nTrying again...\n")

        # waits to restart loop
        time.sleep(30)

    # Waits the set amount of hours to send news update
    hours_wait = 24
    time.sleep(3600 * hours_wait)
