#!/usr/bin/env python

# Copyright 2016 Melomap (www.melomap.com)
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

#
# Thanks http://www.itu.int/dms_pub/itu-t/oth/02/02/T02020000920004PDFE.pdf
# https://www.numberingplans.com/?page=plans&sub=phonenr&alpha_2_input=MM&current_page=74
#

import re


class MMPhoneNumber:

    OOREDOO = "Ooredoo"
    TELENOR = "Telenor"
    MPT = "MPT"
    UNKNOWN = "Unknown"

    GSM_TYPE = "GSM"
    WCDMA_TYPE = "WCDMA"
    CDMA_450_TYPE = "CDMA 450 MHz"
    CDMA_800_TYPE = "CDMA 800 MHz"

    ooredoo_re = r"^(0?9|\+?959)9(7|6)\d{7}$"
    telenor_re = r"^(0?9|\+?959)7(9|8|7)\d{7}$"
    mpt_re = r"^(0?9|\+?959)(5\d{6}|4\d{7,8}|2\d{6,8}|3\d{7,8}|6\d{6}|8\d{6}|7\d{7}|9(0|1|9)\d{5,6})$"

    @classmethod
    def is_valid_mm_phonenumber(cls, phonenumber=None):
        phonenumber = str(phonenumber)
        if phonenumber:
            phonenumber = cls.sanitize_phonenumber(phonenumber=phonenumber)
            mm_phone_re = r"^(0?9|\+?950?9|\+?95950?9)\d{7,9}$"

            if cls.__check_regex([mm_phone_re], phonenumber):
                return True

        return False

    @classmethod
    def sanitize_phonenumber(cls, phonenumber=None):
        phonenumber = str(phonenumber)
        if phonenumber:
            phonenumber = phonenumber.strip()
            phonenumber = phonenumber.replace(" ", "")
            phonenumber = phonenumber.replace("-", "")

            country_code_re = r"^\+?950?9\d+$"

            if cls.__check_regex([country_code_re], phonenumber):
                # try to remove double country code
                double_country_code_re = r"^\+?95950?9\d{7,9}$"

                if cls.__check_regex([double_country_code_re], phonenumber):
                    # remove double country code
                    phonenumber = phonenumber.replace("9595", "95", 1)

                # remove 0 before area code
                zero_before_areacode_re = r"^\+?9509\d{7,9}$"

                if cls.__check_regex([zero_before_areacode_re], phonenumber):
                    # remove double country code
                    phonenumber = phonenumber.replace("9509", "959", 1)

        return phonenumber

    @classmethod
    def get_telecom_name(cls, phonenumber=None):
        phonenumber = str(phonenumber)
        telecom_name = cls.UNKNOWN

        if phonenumber and cls.is_valid_mm_phonenumber(
            phonenumber=phonenumber
        ):
            # sanitize the phonenumber first
            phonenumber = cls.sanitize_phonenumber(phonenumber=phonenumber)

            if cls.__check_regex([cls.ooredoo_re], phonenumber):
                telecom_name = cls.OOREDOO
            elif cls.__check_regex([cls.telenor_re], phonenumber):
                telecom_name = cls.TELENOR
            elif cls.__check_regex([cls.mpt_re], phonenumber):
                telecom_name = cls.MPT

        return telecom_name

    @classmethod
    def get_phone_network_type(cls, phonenumber=None):
        phonenumber = str(phonenumber)
        network_type = cls.UNKNOWN

        if phonenumber and cls.is_valid_mm_phonenumber(
            phonenumber=phonenumber
        ):
            # sanitize the phonenumber first
            phonenumber = cls.sanitize_phonenumber(phonenumber=phonenumber)

            if cls.__check_regex(
                [cls.ooredoo_re, cls.telenor_re], phonenumber
            ):
                network_type = cls.GSM_TYPE
            elif cls.__check_regex([cls.mpt_re], phonenumber):
                wcdma_re = r"^(09|\+?959)(55\d{5}|25[2-4]\d{6}|26\d{7}|4(4|5|6)\d{7})$"
                cdma_450_re = r"^(09|\+?959)(8\d{6}|6\d{6}|49\d{6})$"
                cdma_800_re = r"^(09|\+?959)(3\d{7}|73\d{6}|91\d{6})$"

                if cls.__check_regex([wcdma_re], phonenumber):
                    network_type = cls.WCDMA_TYPE
                elif cls.__check_regex([cdma_450_re], phonenumber):
                    network_type = cls.CDMA_450_TYPE
                elif cls.__check_regex([cdma_800_re], phonenumber):
                    network_type = cls.CDMA_800_TYPE
                else:
                    network_type = cls.GSM_TYPE

        return network_type

    @classmethod
    def __check_regex(cls, regex_array, input_string):
        for regex in regex_array:
            if re.search(regex, input_string):
                return True

        return False
