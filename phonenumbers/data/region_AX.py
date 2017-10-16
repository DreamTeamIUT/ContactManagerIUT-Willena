"""Auto-generated file, do not edit by hand. AX metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_AX = PhoneMetadata(id='AX', country_code=358, international_prefix='00|99(?:[02469]|5(?:11|33|5[59]|88|9[09]))',
    general_desc=PhoneNumberDesc(national_number_pattern='[135]\\d{5,9}|[27]\\d{4,9}|4\\d{5,10}|6\\d{7,8}|8\\d{6,9}', possible_number_pattern='\\d{5,12}', possible_length=(5, 6, 7, 8, 9, 10, 11, 12)),
    fixed_line=PhoneNumberDesc(national_number_pattern='18[1-8]\\d{3,9}', possible_number_pattern='\\d{6,12}', example_number='1812345678', possible_length=(6, 7, 8, 9, 10, 11, 12)),
    mobile=PhoneNumberDesc(national_number_pattern='4\\d{5,10}|50\\d{4,8}', possible_number_pattern='\\d{6,11}', example_number='412345678', possible_length=(6, 7, 8, 9, 10, 11)),
    toll_free=PhoneNumberDesc(national_number_pattern='800\\d{4,7}', possible_number_pattern='\\d{7,10}', example_number='8001234567', possible_length=(7, 8, 9, 10)),
    premium_rate=PhoneNumberDesc(national_number_pattern='[67]00\\d{5,6}', possible_number_pattern='\\d{8,9}', example_number='600123456', possible_length=(8, 9)),
    shared_cost=PhoneNumberDesc(),
    personal_number=PhoneNumberDesc(),
    voip=PhoneNumberDesc(),
    pager=PhoneNumberDesc(),
    uan=PhoneNumberDesc(national_number_pattern='[13]0\\d{4,8}|2(?:0(?:[016-8]\\d{3,7}|[2-59]\\d{2,7})|9\\d{4,8})|60(?:[12]\\d{5,6}|6\\d{7})|7(?:1\\d{7}|3\\d{8}|5[03-9]\\d{2,7})', possible_number_pattern='\\d{5,10}', example_number='10112345', possible_length=(5, 6, 7, 8, 9, 10)),
    voicemail=PhoneNumberDesc(),
    no_international_dialling=PhoneNumberDesc(national_number_pattern='[13]00\\d{3,7}|2(?:0(?:0\\d{3,7}|2[023]\\d{1,6}|9[89]\\d{1,6}))|60(?:[12]\\d{5,6}|6\\d{7})|7(?:1\\d{7}|3\\d{8}|5[03-9]\\d{2,7})', possible_number_pattern='\\d{5,10}', example_number='100123', possible_length=(5, 6, 7, 8, 9, 10)),
    preferred_international_prefix='00',
    national_prefix='0',
    national_prefix_for_parsing='0')