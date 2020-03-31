import send_wiki
import use_files
import time


print("\n[forever_send_wiki] Starting send_wiki.py")
while 1:
    try:
        send_wiki.main()

    except Exception as e:
        # saves error file
        use_files.basic_write_file("forever_send_wiki_crash_report", "send_wiki crashed with the exception: " + str(e))

        print("\n[forever_send_wiki] The error: '" + str(e) +
              "' occurred while running send_wiki.py.\nTrying again...\n")

        # waits to restart loop
        time.sleep(30)

    # Waits set amount of hours to send news update

    hours_wait = 24
    time.sleep(3600 * hours_wait)
