from booking.booking import Booking
import time



booking = Booking()


with booking:
    booking.open_page()
    # booking.change_currency(currency="USD")
    booking.input_values(input("Where you want to go?"),input("What is the checkin date?"), input("What is the checkout date?"),
        rooms=int(input("How many rooms?",)),
        adults=int(input("How many adults?",)),
        children=int(input("How many children?",)),
        ) # dont give zero
    print("Searching...Please wait a minute")
    booking.implicitly_wait(2)
    booking.search()
    booking.implicitly_wait(2)
    # booking.apply_filtration(rating=3)
    booking.low_to_high()
    booking.refresh()
    booking.report_list()
    time.sleep(5)
    



