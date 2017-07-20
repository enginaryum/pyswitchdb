from switch_client import Model
from field import *

class User(Model):
    isActive = Bool(default=False)
    registeredDate = Date(default=datetime.datetime.now())
    userName =  String()
    userSurname =  String()
    userPhone =  String()
    userMail =  String()
    userBirthday = Date()
    TCKN =  String(max_length=11)
    password =  String(max_length=128)
    isRemoved =  String(max_length=128)

class UserToken(Model):
    _type = String(max_length=1)
    user_id = String(required=True)
    user = [ObjectID()]
    user = Array(ObjectID(ref='Property'))
    token = String()

class Property(Model):
    propertyCategory = String()
    propertyType = String()
    isOpportunity = Bool()
    property_id = Integer()
    sellerType = String()
    isDivided = Bool()
    deedInfo = String()
    pafta = Integer()
    ada = Integer()
    parsel = Integer()
    isCredible = Bool()
    deedFee = String()
    VAT = String()
    photos = Array()

class Land(Model):
    width = Integer()
    plantingType = String()
    imar = String()
    emsal = Integer()
    gabari = Integer()


class Base4Wall(Model):
    age = Integer()
    netArea = Integer()
    landArea = Integer()
    number_room = String()
    buildingType = String()
    buildingState = String()
    number_all_flats = Integer()
    number_the_flat = Integer()
    heatingSystem = String()
    number_bath = Integer()
    number_balcony = Integer()
    roofHeight = Integer()
    parkingArea = String()
    renterState = Bool()
    rentIncome = Integer()
    monthlyFee = Integer()
    independentSection = Integer()

    class Meta:
        abstract = True


class House(Base4Wall):
    number_bath = Integer()


class Commercial(Base4Wall):
    devren = Bool()


class Auction(Model):
    state = String(required=True, max_length=128)
    notificationHandled = Bool()
    startingPrice = Integer()
    minimumSellingPrice = Integer()
    reportPrice = Integer()
    minimumRiseAmount = Integer()
    lastGivingPrice = Integer()
    serviceFee = Integer()
    number_auction = Integer()
    startDate = Integer()
    endDate = Date()


class Notification(Model):
    content = String()
    header = String()


class GoogleMapsInfo(Model):
    x = String()
    y = String()


class AuctionOffer(Model):
    amount = Integer()


class HavaleToken(Model):
    pass


class UserLog(Model):
    pass


class ContactForm(Model):
    pass


class ActivityLog(Model):
    pass


class Media(Model):
    pass


class UserSettings(Model):
    smsActive = Bool()
    mailActive = Bool()
    subsActive = Bool()


class Conversation(Model):
    pass


class ExpertiseCompany(Model):
    pass


class SavedFilter(Model):
    type = String()


class ExpertiseRequest(Model):
    isHandled = Bool()


class Subscription(Model):
    list = String()
    user = Integer()


class RDB(Model):
    pass


class Message(Model):
    pass


class MailList(Model):
    subject = String()


class ExpertiseOffer(Model):
    status = Bool()


class BuyerProfile(Model):
    paidDeposit = Bool()
    isWinner = Bool()


class Address(Model):
    city = String()
    district = String()
    semt = String()
    fullAddress = String()



