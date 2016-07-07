#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Import all of the admins from submodules and thread them together.
"""
from calaccess_raw.admin.base import BaseAdmin
from calaccess_raw.admin.campaign import (
    CvrSoCdAdmin,
    Cvr2SoCdAdmin,
    CvrCampaignDisclosureCdAdmin,
    Cvr2CampaignDisclosureCdAdmin,
    RcptCdAdmin,
    Cvr3VerificationInfoCdAdmin,
    LoanCdAdmin,
    S401CdAdmin,
    ExpnCdAdmin,
    F495P2CdAdmin,
    DebtCdAdmin,
    S496CdAdmin,
    S497CdAdmin,
    F501502CdAdmin,
    S498CdAdmin,
)
from calaccess_raw.admin.inactive import (
    BallotMeasuresCdAdmin,
    CvrF470CdAdmin,
    FilerTypePeriodsCd,
    LobbyistContributions1CdAdmin,
    LobbyistContributions2CdAdmin,
    LobbyistContributions3CdAdmin,
    LobbyistEmpLobbyist1CdAdmin,
    LobbyistEmpLobbyist2CdAdmin,
    LobbyistEmployer1CdAdmin,
    LobbyistEmployer2CdAdmin,
    LobbyistEmployer3CdAdmin,
    LobbyistEmployerFirms1CdAdmin,
    LobbyistEmployerFirms2CdAdmin,
    LobbyistEmployerHistoryCdAdmin,
    LobbyistFirm1CdAdmin,
    LobbyistFirm2CdAdmin,
    LobbyistFirm3CdAdmin,
    LobbyistFirmEmployer1CdAdmin,
    LobbyistFirmEmployer2CdAdmin,
    LobbyistFirmHistoryCdAdmin,
    LobbyistFirmLobbyist1CdAdmin,
    LobbyistFirmLobbyist2CdAdmin,
    EfsFilingLogCdAdmin,
)
from calaccess_raw.admin.lobbying import (
    CvrRegistrationCdAdmin,
    Cvr2RegistrationCdAdmin,
    CvrLobbyDisclosureCdAdmin,
    Cvr2LobbyDisclosureCdAdmin,
    LobbyAmendmentsCdAdmin,
    F690P2CdAdmin,
    LattCdAdmin,
    LexpCdAdmin,
    LccmCdAdmin,
    LothCdAdmin,
    LempCdAdmin,
    LpayCdAdmin,
    LobbyingChgLogCdAdmin
)
from calaccess_raw.admin.common import (
    FilernameCdAdmin,
    FilerFilingsCdAdmin,
    FilingsCdAdmin,
    SmryCdAdmin,
    CvrE530CdAdmin,
    SpltCdAdmin,
    TextMemoCdAdmin,
    AcronymsCdAdmin,
    AddressCdAdmin,
    FilersCdAdmin,
    FilerAcronymsCdAdmin,
    FilerAddressCdAdmin,
    FilerEthicsClassCdAdmin,
    FilerInterestsCdAdmin,
    FilerLinksCdAdmin,
    FilerStatusTypesCdAdmin,
    FilerToFilerTypeCdAdmin,
    FilerTypesCdAdmin,
    FilerXrefCdAdmin,
    FilingPeriodCdAdmin,
    GroupTypesCdAdmin,
    HeaderCdAdmin,
    HdrCdAdmin,
    ImageLinksCdAdmin,
    LegislativeSessionsCdAdmin,
    LookupCodesCdAdmin,
    NamesCdAdmin,
    ReceivedFilingsCdAdmin,
    ReportsCdAdmin,
)

from calaccess_raw.admin.tracking import (
    RawDataVersionAdmin,
    RawDataFileAdmin,
    RawDataCommandAdmin
)

__all__ = (
    'BaseAdmin',
    'CvrSoCdAdmin',
    'Cvr2SoCdAdmin',
    'CvrCampaignDisclosureCdAdmin',
    'Cvr2CampaignDisclosureCdAdmin',
    'RcptCdAdmin',
    'Cvr3VerificationInfoCdAdmin',
    'LoanCdAdmin',
    'S401CdAdmin',
    'ExpnCdAdmin',
    'F495P2CdAdmin',
    'DebtCdAdmin',
    'S496CdAdmin',
    'SpltCdAdmin',
    'S497CdAdmin',
    'F501502CdAdmin',
    'S498CdAdmin',
    'CvrF470CdAdmin',
    'CvrRegistrationCdAdmin',
    'Cvr2RegistrationCdAdmin',
    'CvrLobbyDisclosureCdAdmin',
    'Cvr2LobbyDisclosureCdAdmin',
    'LobbyAmendmentsCdAdmin',
    'F690P2CdAdmin',
    'LattCdAdmin',
    'LexpCdAdmin',
    'LccmCdAdmin',
    'LothCdAdmin',
    'LempCdAdmin',
    'LpayCdAdmin',
    'FilerFilingsCdAdmin',
    'FilingsCdAdmin',
    'SmryCdAdmin',
    'CvrE530CdAdmin',
    'TextMemoCdAdmin',
    'AcronymsCdAdmin',
    'AddressCdAdmin',
    'BallotMeasuresCdAdmin',
    'EfsFilingLogCdAdmin',
    'FilernameCdAdmin',
    'FilersCdAdmin',
    'FilerAcronymsCdAdmin',
    'FilerAddressCdAdmin',
    'FilerEthicsClassCdAdmin',
    'FilerInterestsCdAdmin',
    'FilerLinksCdAdmin',
    'FilerStatusTypesCdAdmin',
    'FilerToFilerTypeCdAdmin',
    'FilerTypesCdAdmin',
    'FilerXrefCdAdmin',
    'FilingPeriodCdAdmin',
    'FilerTypePeriodsCd',
    'GroupTypesCdAdmin',
    'HeaderCdAdmin',
    'HdrCdAdmin',
    'ImageLinksCdAdmin',
    'LegislativeSessionsCdAdmin',
    'LobbyingChgLogCdAdmin',
    'LobbyistContributions1CdAdmin',
    'LobbyistContributions2CdAdmin',
    'LobbyistContributions3CdAdmin',
    'LobbyistEmployer1CdAdmin',
    'LobbyistEmployer2CdAdmin',
    'LobbyistEmployer3CdAdmin',
    'LobbyistEmployerFirms1CdAdmin',
    'LobbyistEmployerFirms2CdAdmin',
    'LobbyistEmpLobbyist1CdAdmin',
    'LobbyistEmpLobbyist2CdAdmin',
    'LobbyistFirm1CdAdmin',
    'LobbyistFirm2CdAdmin',
    'LobbyistFirm3CdAdmin',
    'LobbyistFirmEmployer1CdAdmin',
    'LobbyistFirmEmployer2CdAdmin',
    'LobbyistFirmLobbyist1CdAdmin',
    'LobbyistFirmLobbyist2CdAdmin',
    'LobbyistFirmHistoryCdAdmin',
    'LobbyistEmployerHistoryCdAdmin',
    'LookupCodesCdAdmin',
    'NamesCdAdmin',
    'ReceivedFilingsCdAdmin',
    'ReportsCdAdmin',
    'RawDataVersionAdmin',
    'RawDataFileAdmin',
    'RawDataCommandAdmin',
)
