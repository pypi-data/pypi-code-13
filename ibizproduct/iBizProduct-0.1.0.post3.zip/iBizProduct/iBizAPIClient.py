from __future__ import unicode_literals
from datetime import *
import itertools
from future.utils import raise_with_traceback
from future.utils import viewitems
from builtins import dict, int, str, bool
from iBizProduct.Contracts.iBizAPIClientInterface import *
from iBizProduct.Contracts.ProductOrderSpec import *
from iBizProduct.Contracts.ProductOrderInfoToReturn import *
from iBizProduct.Contracts.CaseSpec import *
from iBizProduct.Contracts.EventStatus import *
from iBizProduct.Contracts.ProductAuthentication import *
from iBizProduct.iBizBE import *

class iBizAPIClient(iBizAPIClientInterface):

    def __init__(self, externalKey, productId, backend):
        self._ExternalKey = externalKey
        self._ProductId = productId
        self._isDev = backend.IsDev
        if backend != None and not isinstance(backend,iBizBE):
            raise_with_traceback(ValueError('You must supply a valid backend instance'))
        else:
            self._backend = backend

    #https://backend.ibizapi.com:8888/SOAP/CommerceManager/ProductManager/ProductOrder.html#functionExternalAdd
    def ProductOrderAdd(self, productOrderSpec, productId = None):
        self.VerifyExternalKey()

        if productId == None and self._ProductId == None:
            raise_with_traceback(ValueError('You must supply a valid product id.'))

        if not isinstance(productOrderSpec,ProductOrderSpec):
            raise_with_traceback(ValueError('You must supply a valid product order spec.'))

        params = dict(external_key=self._ExternalKey, 
                    product_id=productId or self._ProductId, 
                    productorder_spec=productOrderSpec.getSpec())
        return self._backend.call('CommerceManager/ProductManager/ProductOrder', 'ExternalAdd', params)

    #https://backend.ibizapi.com:8888/SOAP/CommerceManager/ProductManager/ProductOrder.html#functionExternalEdit
    def ProductOrderEdit(self, productOrderId, productOrderSpec):
        self.VerifyExternalKey()

        if not isinstance(productOrderSpec,ProductOrderSpec):
            raise_with_traceback(ValueError('You must supply a valid product order spec.'))

        params = dict(external_key=self._ExternalKey, 
                    productorder_id=productOrderId, 
                    productorder_spec=productOrderSpec.getSpec())
        return self._backend.call('CommerceManager/ProductManager/ProductOrder', 'ExternalEdit', params)

    #https://backend.ibizapi.com:8888/SOAP/CommerceManager/ProductManager/ProductOrder.html#functionExternalView
    def ProductOrderView(self, productOrderId, infoToReturn = None):
        self.VerifyExternalKey()

        if infoToReturn != None and not isinstance(infoToReturn,ProductOrderInfoToReturn):
            raise_with_traceback(ValueError('You must supply a valid infor to return value'))

        params = dict(external_key=self._ExternalKey, productorder_id=productOrderId)
        params = self.__FilterDict(params)

        if infoToReturn != None:
            params['info_to_return'] = infoToReturn.getSpec()

        return self._backend.call('CommerceManager/ProductManager/ProductOrder', 'ExternalView', params)

    #https://backend.ibizapi.com:8888/SOAP/CommerceManager/ProductManager/ProductOrder.html#functionExternalBillOrderAddOneTime
    def ProductOrderBillOrderAddOneTime(self, cycleBeginDate, cycleEndDate, oneTimeCost, productOrderId, 
                                        detailAddon = None, descriptionAddon = None, dueNow = 0):
        self.VerifyExternalKey()

        if not isinstance(cycleBeginDate, datetime) or not isinstance(cycleEndDate,datetime):
            raise_with_traceback(ValueError('You must supply a valid cycle begin and end date value'))

        params = dict(external_key = self._ExternalKey,
                    productorder_id = productOrderId,
                    cycle_begin_date = cycleBeginDate.timestamp(),
                    cycle_end_date = cycleEndDate.timestamp(),
                    one_time_cost = oneTimeCost,
                    detail_addon = detailAddon,
                    description_addon = descriptionAddon,
                    due_now = dueNow)
        params = self.__FilterDict(params)
        return self._backend.call('CommerceManager/ProductManager/ProductOrder', 'ExternalBillOrderAddOneTime', params)

    #https://backend.ibizapi.com:8888/SOAP/CommerceManager/ProductOffer/PurchaseOrder.html#functionExternalAdd
    def PurchaseOrderAdd(self, accountId, offerChain, purchaseOrderSpec, orderName = ''):
        self.VerifyExternalKey()

        params = dict(external_key = self._ExternalKey,
                    offer_chain = offerChain,
                    purhcaseorder_spec = purchaseOrderSpec,
                    order_name = orderName)
        return self._backend.call('CommerceManager/ProductManager/ProductOrder', 'ExternalAdd', params)

    #https://backend.ibizapi.com:8888/SOAP/CommerceManager/ProductOffer/PurchaseOrder.html#functionExternalEdit
    def PurchaseOrderEdit(self, purchaseOrderId, offerChain, purchaseOrderSpec):
        self.VerifyExternalKey()

        params = dict(external_key = self._ExternalKey,
                    offer_chain = offerChain,
                    purchaseorder_spec = purchaseOrderSpec,
                    purchaseorder_id = purchaseOrderId)
        return self._backend.call('CommerceManager/ProductManager/ProductOrder', 'ExternalEdit', params)

    #https://backend.ibizapi.com:8888/SOAP/CommerceManager/ProductOffer/PurchaseOrder.html#functionExternalListOnAccount
    def PurchaseOrderListOnAccount(self, accountId, limit = {}):
        self.VerifyExternalKey()

        params = dict(external_key = self._ExternalKey,
                    account_id = accountId)
        if limit.__len__() > 0:
            params['limit'] = limit

        return self._backend.call('CommerceManager/ProductOffer/PurchaseOrder', 'ExternalListOnAccount', params)

    #https://backend.ibizapi.com:8888/SOAP/CommerceManager/ProductOffer/PurchaseOrder.html#functionExternalGetCycleDelimiters
    def PurchaseOrderCycleDelimiters(self, purchaseOrderId):
        self.VerifyExternalKey()

        params = dict(external_key = self._ExternalKey,
                    purchaseorder_id = purchaseOrderId)

        return self._backend.call('CommerceManager/ProductOffer/PurchaseOrder', 'ExternalGetCycleDelimiters', params)

    #https://backend.ibizapi.com:8888/SOAP/CommerceManager/ProductOffer/PurchaseOrder.html#functionExternalPriceFromPurchase
    def PurchaseOrderPrice(self, purchaseOrderId, accountId):
        self.VerifyExternalKey()

        params = dict(external_key = self._ExternalKey,
                    purchaseorder_id = purchaseOrderId,
                    account_id = accountId)
        
        return self._backend.call('CommerceManager/ProductOffer/PurchaseOrder', 'ExternalPriceFromPurchase', params)

    #https://backend.ibizapi.com:8888/SOAP/CommerceManager/ProductManager/ProductOrder.html#functionExternalOpenCaseWithOwner
    def ProductOpenCaseWithOwner(self, productOrderId, caseSpec):
        self.VerifyExternalKey()

        if not isinstance(caseSpec, CaseSpec):
            raise_with_traceback(ValueError('You must supply a valid case spec object'))

        params = dict(external_key = self._ExternalKey,
                    productorder_id = productOrderId,
                    case_spec = caseSpec.getSpec())
        params = self.__FilterDict(params)
        result = self._backend.call('CommerceManager/ProductManager/ProductOrder', 'ExternalOpenCaseWithOwner', params)

        return result.get('new_id')

    #https://backend.ibizapi.com:8888/SOAP/CommerceManager/ProductManager/ProductOrder.html#functionExternalUpdateCaseWithOwner
    def ProductUpdateCaseWithOwner(self, productOrderId, caseId, caseSpec):
        self.VerifyExternalKey()

        if not isinstance(caseSpec, CaseSpec):
            raise_with_traceback(ValueError('You must supply a valid case spec object'))

        params = dict(external_key = self._ExternalKey,
                    productorder_id = productOrderId,
                    case_spec = caseSpec.getSpec(),
                    case_id = caseId)
        params = self.__FilterDict(params)
        result = self._backend.call('CommerceManager/ProductManager/ProductOrder', 'ExternalUpdateCaseWithOwner', params)

        return result.get('effected_rows')

    #https://backend.ibizapi.com:8888/SOAP/CommerceManager/ProductOffer.html#functionExternalProductPrice
    def ProductOfferPrice(self, productOfferId, accountHost, accountId = None):
        self.VerifyExternalKey()
        
        params = dict(external_key = self._ExternalKey,
                    account_host = accountHost,
                    productoffer_id = productOfferId,
                    account_id = accountId)
        params = self.__FilterDict(params)


        return self._backend.call('CommerceManager/ProductOffer', 'ExternalProductPrice', params)

    #https://backend.ibizapi.com:8888/SOAP/CommerceManager/ProductManager/ProductOrder.html#functionExternalGetNextChargeDate
    def ProductOrderNextChargeDate(self, productOrderId):
        self.VerifyExternalKey()

        params = dict(external_key = self._ExternalKey,
                    productorder_id = productOrderId)
        params = self.__FilterDict(params)
        result = self._backend.call('CommerceManager/ProductManager/ProductOrder', 'ExternalGetNextChargeDate', params)

        return result.get('next_charge_date')

    #https://backend.ibizapi.com:8888/JSON/CommerceManager/ProductManager/ProductOrder.html#ExternalNonCurrentAccounts
    def ProductOrderNonCurrentAccounts(self, productOrderId):
        self.VerifyExternalKey()

        params = dict(external_key = self._ExternalKey,
                    productorder_id = productOrderId)
        params = self.__FilterDict(params)
        result = self._backend.call('CommerceManager/ProductManager/ProductOrder', 'ExternalNonCurrentAccounts', params)
        
        return result.get('data')

    #https://backend.ibizapi.com:8888/JSON/CommerceManager/ProductManager?action=ExternalListPurchases
    def ListPurchases(self, limit = None, amount = None, start = None, sort = None):
        self.VerifyExternalKey()

        params = dict(external_key = self._ExternalKey,
                    limit = limit,
                    many = amount,
                    product_id = self._ProductId,
                    sort_by = sort,
                    start = start)
        params = self.__FilterDict(params)
        result = self._backend.call('CommerceManager/ProductManager', 'ExternalListPurchases', params)

        error = result.get('error')
        if error != None:
            raise_with_traceback(ValueError(error))
        
        return result.get('LIST')

    #https://backend.ibizapi.com:8888/SOAP/CommerceManager/ProductManager/ProductOrder.html#functionExternalGetOwnerLanguage
    def ProductOrderOwnerLanguage(self, productOrderId):
        self.VerifyExternalKey()

        params = dict(external_key = self._ExternalKey,
                    productorder_id = self._ProductId)
        params = self.__FilterDict(params)
        
        return self._backend.call('CommerceManager/ProductManager/ProductOrder', 'ExternalGetOwnerLanguage', params)

    #https://backend.ibizapi.com:8888/SOAP/CommerceManager/ProductManager/ProductOrder.html#functionExternalProductOrderPricing
    def ProductOrderPricing(self, productOrderId):
        self.VerifyExternalKey()

        params = dict(external_key = self._ExternalKey,
                    productorder_id = self._ProductId)
        params = self.__FilterDict(params)

        return self._backend.call('CommerceManager/ProductManager/ProductOrder', 'ExternalProductOrderPricing', params)
    
    #https://backend.ibizapi.com:8888/SOAP/CommerceManager/ProductManager/ProductOrder.html#functionExternalUpdateInventory
    def ProductOrderUpdateInventory(self, productOrderId, inventoryData):
        self.VerifyExternalKey()

        params = dict(external_key = self._ExternalKey,
                    inventory_data = inventoryData,
                    productorder_id = productOrderId)
        params = self.__FilterDict(params)

        return self._backend.call('CommerceManager/ProductManager/ProductOrder', 'ExternalUpdateInventory', params)

    def UpdateEvent(self, eventId, status, message):
        self.VerifyExternalKey()

        params = dict(external_key = self._ExternalKey,
                    productorderevent_id = eventId,
                    message = message,
                    status = status)
        params = self.__FilterDict(params)                      
        result = self._backend.call('CommerceManager/ProductManager/ProductOrder/Event', 'ExternalUpdateEvent', params)

        return result.get('success')

    def AuthenticateUser(self, productOrderAuthentication):
        pass

    def IsValidBackendRequest(self, externalKey):
        self.VerifyExternalKey()

        if self._ExternalKey != externalKey:
            raise_with_traceback(ValueError("Your request was not authorized. If you continue to see this message you're doing it wrong..."))

        return True

    def VerifyExternalKey(self):
        if not self.ExternalKeyExists():
            raise_with_traceback(ValueError("""Your Products External Key was not found or is not accessible. Please verify that the key is set in the AppSettings " +
                "section of your config file. You can find the Product External Key in the Panel under the External Attributes section " +
                "of the ProductEdit page."""))

    def ExternalKeyExists(self):
        return self._ExternalKey != None

    def __FilterDict(self, dictionary):
        for item in viewitems(dictionary.copy()):
            if item[1] == None:
                del dictionary[item[0]]

        return dictionary
