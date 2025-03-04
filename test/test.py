from ..class.Accomodation import Accommodation
from ..class.datetime import datetime
from ..class.Booking import Booking
from ..class.User import Member

new_acc = Accommodation("test", "location", "description", 0)
print(new_acc.get_acc_name)

new_member = Member('tord','saygex@gaymail.com','1234','123456789',18)

new_book = Booking(accom=new_acc, date=datetime.now(), guess=0, member=new_member)

print(new_book.get_member.get_user_name)