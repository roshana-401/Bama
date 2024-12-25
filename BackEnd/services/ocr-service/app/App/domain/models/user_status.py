from enum import Enum


class UserStatus(str, Enum):
    unverified  = "unverified"
    verified  = "verified"
    active  = "active"
    inactive = "inactive"
