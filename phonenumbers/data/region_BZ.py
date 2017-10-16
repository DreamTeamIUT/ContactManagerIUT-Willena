"""Auto-generated file, do not edit by hand. BZ metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_BZ = PhoneMetadata(id='BZ', country_code=501, international_prefix='00',
    general_desc=PhoneNumberDesc(national_number_pattern='[2-8]\\d{6}|0\\d{10}', possible_number_pattern='\\d{7}(?:\\d{4})?', possible_length=(7, 11)),
    fixed_line=PhoneNumberDesc(national_number_pattern='(?:[23458][02]\\d|7(?:[02]\\d|32))\\d{4}', possible_number_pattern='\\d{7}', example_number='2221234', possible_length=(7,)),
    mobile=PhoneNumberDesc(national_number_pattern='6[0-35-7]\\d{5}', possible_number_pattern='\\d{7}', example_number='6221234', possible_length=(7,)),
    toll_free=PhoneNumberDesc(national_number_pattern='0800\\d{7}', possible_number_pattern='\\d{11}', example_number='08001234123', possible_length=(11,)),
    premium_rate=PhoneNumberDesc(),
    shared_cost=PhoneNumberDesc(),
    personal_number=PhoneNumberDesc(),
    voip=PhoneNumberDesc(),
    pager=PhoneNumberDesc(),
    uan=PhoneNumberDesc(),
    voicemail=PhoneNumberDesc(),
    no_international_dialling=PhoneNumberDesc(),
    number_format=[NumberFormat(pattern='(\\d{3})(\\d{4})', format='\\1-\\2', leading_digits_pattern=['[2-8]']),
        NumberFormat(pattern='(0)(800)(\\d{4})(\\d{3})', format='\\1-\\2-\\3-\\4', leading_digits_pattern=['0'])],
    leading_zero_possible=True)