from enum import Enum

class ItemType(str, Enum):
    CURRENCY = 'currency'
    TEXT = 'text'
    PERCENTAGE = 'percentage'
    DATE = 'date'

class ItemStatus(str, Enum):
    OK = 'ok'
    WARNING = 'warning'
    CRITICAL = 'critical'

class AssetType(str, Enum):
    DEFAULT = 'default'
    # Finance
    CURRENT_ACCOUNT = 'current_account'
    SAVINGS = 'savings'
    INVESTMENTS = 'investments'
    DEBT = 'debt'
    # Real Estate
    HOUSE = 'house'
    APARTMENT = 'apartment'
    LAND = 'land'
    PARKING = 'parking'
    # Vehicles
    CAR = 'car'
    MOTORBIKE = 'motorbike'
    BOAT = 'boat'
    PLANE = 'plane'
    # Career
    JOB = 'job'
    FREELANCE = 'freelance'
    EDUCATION = 'education'
    SKILL = 'skill'
    # Health
    MEDICAL = 'medical'
    SPORT = 'sport'
    INSURANCE = 'insurance'
    AMBULANCE = 'ambulance'
    HOSPITAL = 'hospital'
    DOCTOR = 'doctor'
    # Hobbies
    TRAVEL = 'travel'
    HOBBY_CREATIVE = 'hobby_creative'
    HOBBY_TECH = 'hobby_tech'
    # Social
    FAMILY = 'family'
    FRIENDS = 'friends'
    PET = 'pet'
    BENCH = 'bench'
    GIFT = 'gift'
    PHONE = 'phone'
    # Legacy / Fallbacks
    FINANCE = 'finance'
    HEALTH = 'health'
    HOME = 'home'
    NATURE = 'nature'
    TECH = 'tech'
    PEOPLE = 'people'
    # Items / Tools
    WRENCH = 'wrench'
    SCREWS = 'screws'

class WidgetType(str, Enum):
    HISTORY = 'history'
    SUBSCRIPTIONS = 'subscriptions'
    GOALS = 'goals'
    MAINTENANCE = 'maintenance'
    DEADLINES = 'deadlines'
    PROPERTY = 'property'
    ENERGY = 'energy'
    SOCIAL_CALENDAR = 'social-calendar'
    BIRTHDAYS = 'birthdays'
    CONTACTS = 'contacts'
    HEALTH_BODY = 'health-body'
    HEALTH_APPOINTMENTS = 'health-appointments'

class HistoryCategory(str, Enum):
    INCOME = 'income'
    EXPENSE = 'expense'
    TRANSFER = 'transfer'

class MaintenanceUrgency(str, Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    CRITICAL = 'critical'

class SocialEventType(str, Enum):
    PARTY = 'party'
    DINNER = 'dinner'
    WEDDING = 'wedding'
    BIRTHDAY = 'birthday'
    OTHER = 'other'

class HealthAppointmentType(str, Enum):
    DOCTOR = 'doctor'
    DENTIST = 'dentist'
    VACCINE = 'vaccine'
    CHECKUP = 'checkup'
    OTHER = 'other'

class AlertSeverity(str, Enum):
    WARNING = 'warning'
    CRITICAL = 'critical'

class RecurringSourceType(str, Enum):
    SUBSCRIPTION = 'subscription'
    SALARY = 'salary'
    RENT = 'rent'
    INSURANCE = 'insurance'
    CUSTOM = 'custom'
