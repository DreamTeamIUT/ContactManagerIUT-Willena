"""Auto-generated file, do not edit by hand. YE metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_YE = PhoneMetadata(id='YE', country_code=None, international_prefix=None,
    general_desc=PhoneNumberDesc(national_number_pattern='1\\d{2}', possible_number_pattern='\\d{3}', possible_length=(3,)),
    toll_free=PhoneNumberDesc(),
    premium_rate=PhoneNumberDesc(),
    emergency=PhoneNumberDesc(national_number_pattern='19[1459]', possible_number_pattern='\\d{3}', example_number='191', possible_length=(3,)),
    short_code=PhoneNumberDesc(national_number_pattern='19[1459]', possible_number_pattern='\\d{3}', example_number='191', possible_length=(3,)),
    standard_rate=PhoneNumberDesc(),
    carrier_specific=PhoneNumberDesc(),
    short_data=True)
