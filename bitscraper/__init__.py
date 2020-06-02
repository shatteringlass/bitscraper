#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Borsa Italiana (Italian Stock Exchanve) market data downloader
# https://github.com/shatteringlass/bit_scraper
#
# Copyright 2017-2020 Federico Pizzolo
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

__version__ = "0.1.0"
__author__ = "Federico Pizzolo"

from .product_listings import BITListing

__all__ = ["BITListing"]