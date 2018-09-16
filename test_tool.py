import sys
from alien_translator import AlienTranslator
from universe import UniverseGod

translator = AlienTranslator("hello world 000")
universe = UniverseGod()

if sys.argv[1] == "enc":
    ans = translator.encrypt_to_code(sys.argv[2])
    with open("out.txt", "w") as file:
        file.write(ans)
    print(ans)

elif sys.argv[1] == "dec":
    with open("out.txt", "r") as file:
        data = file.read()
        data = data.strip("\n")
        ans = translator.decrypt_to_msg(data)
    print(ans)

elif sys.argv[1] == "t_enc":
    with open("out.txt", "r") as file:
        data = file.read()
        data = data.strip("\n")
        ans = universe.gen_future_code("2018-02-01", data)

    with open("time_out.txt", "w") as file:
        file.write(ans)

    print(ans)

elif sys.argv[1] == "t_dec":
    with open("time_out.txt", "r") as file:
        data = file.read()
        data = data.strip("\n")

        date_signature = universe.gen_passed_time_signature("2018-02-01")
        time_translator = AlienTranslator(date_signature)

        ans = time_translator.decrypt_to_msg(data)
        ans = translator.decrypt_to_msg(ans)

    print(ans)
