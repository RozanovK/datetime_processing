from datetime import datetime
import sys

WEEKDAY = {0: 'Poniedziałek',
           1: 'Wtorek',
           2: 'Środę',
           3: 'Czwartek',
           4: 'Piątek',
           5: 'Sobotę',
           6: 'Niedzielę'}


class DT:
    def __init__(self, proc_dt):
        try:
            self.proc_dt = datetime.strptime(proc_dt, '%Y-%m-%d%H:%M:%S')
            self.ref_dt = datetime.now()
            print(self.proc_dt)
        except ValueError:
            raise ValueError("Zły format danych wejściowych, powinno być YYYY-MM-DDH:M:S")

    def compare_dt(self):  # sprawdzamy czy data jest w przyszłości czy w przeszłości
        if self.ref_dt > self.proc_dt:
            cmp = 'p'
        else:
            cmp = 'f'
        return cmp

    def get_HMS(self):                                      # liczymy różnicę czasową miedzy datami
        seconds, minutes, hours, days = 0, 0, 0, 0
        if self.compare_dt() == 'p':
            delta = self.ref_dt - self.proc_dt
        else:
            delta = self.proc_dt - self.ref_dt

        if delta.seconds > 60:  # dzielimy zwrócone sekundy na jednostki czasowe
            minutes, seconds = divmod(delta.seconds, 60)
            if minutes > 60:
                hours, minutes = divmod(minutes, 60)
        days = delta.days
        return seconds, minutes, hours, days

    def processing_weekday(self):
        seconds, minutes, hours, days = self.get_HMS()
        wkd_i = self.proc_dt.weekday()                   # sprawdzamy który dzień tygodnia

        def ext_compare_dt(x, str, week_num):             # rozróżniamy "tydzień temu" i "za tydzień"
            if week_num == 1:
                week_num = ""
            if self.compare_dt() == 'p':
                str = ("%s %s %s temu") % (str, week_num, x)
            else:
                str = ("%s za %s %s") % (str, week_num, x)
            return str

        if days in (0, 1):
            if self.proc_dt.day == self.ref_dt.day:             #sprawdzamy czy to dzisiaj
                str = ("Dzisiaj o %i:%i") % (self.proc_dt.hour, self.proc_dt.minute)
            elif self.proc_dt.day >self.ref_dt.day:
                str = ("Jutro o %i:%i") % (self.proc_dt.hour, self.proc_dt.minute)
            else:
                str = ("Wczoraj o %i:%i") % (self.proc_dt.hour, self.proc_dt.minute)

        elif days < 7:
            if wkd_i in (2, 5, 6):  # jest tylko "ten", a nie "przyszly" "zeszly" ze względu na to jak się mówi potocznie
                x = "tę"
            else:
                x = "ten"
            str = ("W %s %s o %i:%i") % (x, WEEKDAY[wkd_i], self.proc_dt.hour, self.proc_dt.minute)

        elif 7 <= days <= 14:
            if wkd_i in (2, 5, 6):  # sprawdzamy poprawne zakończenie
                x = "ą"
            else:
                x = "y"

            if self.compare_dt() == 'p':
                str = ('w zeszł%c %s o %i:%i') % (x, WEEKDAY[wkd_i], self.proc_dt.hour, self.proc_dt.minute)
            else:
                str = ('w przyszł%c %s o %i:%i') % (x, WEEKDAY[wkd_i], self.proc_dt.hour, self.proc_dt.minute)

        else:
            week_num = int(days/7)
            tue_char = ""
            if wkd_i == 1:                                #dodajemy ten warunek ze względu na "we wtorek"
                tue_char = "e"
            str = ("w%s " + WEEKDAY[wkd_i]) % tue_char
            if week_num == 1:
                x = "tydzień"
            elif week_num in (2,3,4):
                x = "tygodnie"
            else:
                x = "tygodni"
            str = ext_compare_dt(x, str, week_num)
        print(str)

    def processing_in_time(self):
        seconds, minutes, hours, days = self.get_HMS()
        str = ""

        if days != 0:                            # dni się odmieniają inaczej niż godzina/minuta/sekunda, więc osobna pętla
            if days == 1:
                x = "dzień"
            else:
                x = "dni"
            str += ("%i %s ") % (days, x)


        def processing_HMS(str, v, name):        #odpowiednia odmiana HMS
            x = ""
            if v != 0:
                if v == 1:
                    x = "ę"
                elif v in (2, 3, 4) or v % 10 in (2, 3, 4) and v not in (12, 13, 14):
                    x = "y"
                str += ("%i %s%s ") % (v, name, x)
            return str

        str = processing_HMS(str, hours, "godzin")
        str = processing_HMS(str, minutes, "minut")
        str = processing_HMS(str, seconds, "sekund")

        if self.compare_dt() == 'p':
            str += "temu"
        else:
            str = "Za " + str

        print(str)


if __name__ == "__main__":
    x = DT(sys.argv[1])
    x.processing_weekday()
    x.processing_in_time()
