import allure

from automation.tests.workflows.brownfield.aop_flows.aop_flow_cases import *

log = logging.getLogger(__name__)




@pytest.mark.Plv
@pytest.mark.Regression
@pytest.mark.testrail(id=1220586)
def test_set_global_vars():
    """
    ==== This test is called to initialize global test data dictionary
    """
    init_global_test_Data()



@pytest.mark.Regression
@pytest.mark.testrail(id=1220586)
def test_oaas():
    """
    ===== Create IAP device on Activate order process ======
    1. Create_3_Network_devices(IAP, Switch, Gateway)
    """
    #assert Create_oaas_devices(dev_type="STORAGE")
    pass

@allure.parent_suite("activate-sm-workflows")
@allure.suite("Brownfield aop flow cases")
@pytest.mark.Plv
@allure.sub_suite("Brownfield aop flow order test cases for all device types")
class TestAopFlowCases:
    
    @pytest.mark.Regression
    @pytest.mark.testrail(id=1220586)
    def test_Create_3_Network_devices(self):
        """
        ===== Create IAP device on Activate order process ======
        1. Create_3_Network_devices(IAP, Switch, Gateway)
        """
    
        assert Create_devices(dev_type="GATEWAY", part_category="SWITCH")
      #  assert Create_Network_devices(dev_type="IAP", part_category="IAP")
        #assert Create_Network_devices(dev_type="SWITCH", part_category="SWITCH")
    
    
    @pytest.mark.Regression
    @pytest.mark.testrail(id=1220586)
    def test_Create_3_Compute_devices(self):
        """
        ===== Create IAP device on Activate order process ======
        1. Create_3_Compute_devices(COMPUTE,DHCI_COMPUTE,SERVER)
        """
        assert Create_devices(dev_type="COMPUTE", part_category="COMPUTE")
        #assert Create_devices(dev_type="DHCI_COMPUTE", part_category="COMPUTE")
        #assert Create_Compute_devices("SERVER")
    
    
    
    @pytest.mark.Regression
    @pytest.mark.testrail(id=1220586)
    def test_Create_3_Storage_devices(self):
        """
        ===== Create IAP device on Activate order process ======
        1. Create_3_Compute_devices(COMPUTE,DHCI_COMPUTE,SERVER)
        """
        assert Create_devices(dev_type="STORAGE", part_category="STORAGE")
        #assert Create_devices(dev_type="DHCI_COMPUTE", part_category="COMPUTE")
        #assert Create_Compute_devices("SERVER")
    
    
    @pytest.mark.Regression
    @pytest.mark.testrail(id=1220586)
    def test_PointofSalesorder_verifiedalias(self):
        """
        ===== Create Point of sales order with verified alias device on Activate order process ======
        """
        assert Create_Pos("STORAGE",end_username=True)
    
    @pytest.mark.testrail(id=1220586)
    @pytest.mark.Regression
    def test_SalesDirectOrder_verifiedalias(self):
        """
        ===== Create Sales direct shipment order with verified alias enduser name   =====
        """
        assert Create_Sds("STORAGE",end_username=True)
    
    @pytest.mark.testrail(id=1220587)
    @pytest.mark.Regression
    def test_Create_License_Order_Compute_Unverified_Alias(self):
        """
        =====  Create license order for compute devices unverified alias that is used same in Sales orders (order_class: ZSTD) =====
        """
        assert Create_License("COMPUTE")
    
    @pytest.mark.testrail(id=1220589)
    @pytest.mark.Regression
    def test_Create_License_Order_Network_Verified_Alias(self):
        """
        =====    =====
        """
        assert Create_License("IAP",part_category="IAP")
    
    @pytest.mark.testrail(id=1220588)
    @pytest.mark.Regression
    def test_Create_License_Order_Storage_Party_List(self):
        """
        =====   Create license order for Storage devices unverified alias that is used same in Sales orders (order_class: BRIM) =====
        """
        assert Create_License("STORAGE")
    
    @pytest.mark.testrail(id=1220591)
    @pytest.mark.Regression
    def test_Update_device_manufacturing_order_unclaimed (self):
        """
        ===== Send update request to the manufactured device (Firmware version, Status) ====
        """
        assert Update_manufacture("STORAGE",{"fw_version": "2.1"})
    
    @pytest.mark.testrail(id=1220592)
    @pytest.mark.Regression
    def test_Update_device_manufacturing_order_unassigned(self):
        """
        ===== Send update request to the manufactured device (Add extra attributes) ====
        """
        assert Update_manufacture("STORAGE",{"extra_attributes": [{"name": "name1","value": "123"}]})
    
    @pytest.mark.testrail(id=1220593)
    @pytest.mark.Regression
    def test_Update_device_manufacturing_order_assigned_unsubscribed(self):
        """
        =====Send update request to the manufactured device (Add entitlement id)  ====
        """
        assert Update_manufacture("STORAGE",{"entitlement_id": "ABCD"})
    
    @pytest.mark.testrail(id=1220594)
    @pytest.mark.Regression
    def test_Update_device_manufacturing_order_assigned_subscribed(self):
        """
        =====  Send update request to the manufactured device (Add child device)  ====
        """
        assert Update_manufacture_adchild("STORAGE",{})
    
    @pytest.mark.testrail(id=1220595)
    def test_Update_Sales_Direct_Order_Unverified_alias(self):
        """
        =====  Send update request to the sds, add distributor PO number  ====
        """
        assert Update_Sds("STORAGE", { 'customer_po': 'NEW_CUST_PO'})

    @pytest.mark.testrail(id=1220596)
    @pytest.mark.Regression
    def test_Update_PointofSales_order_Verified_alias(self):
        """
        =====  Send  Update point of sales order with increased quantity by 1. ====
        """
        assert Update_Pos("STORAGE", { 'quantity': 2 })
    
    @pytest.mark.testrail(id=1220597)
    @pytest.mark.Regression
    def test_Update_License_Order_Compute_Unverified_Alias(self):
        """
        =====  Update the license order with verified alias end username, add distributor PO number ====
        """
        assert Update_License("COMPUTE", {'reason': 'Update', 'po': 'NEW_PO' })
    
    @pytest.mark.testrail(id=1220598)
    @pytest.mark.Regression
    def test_Update_License_Order_Storage_Additional_License(self):
        """
        ===== Add one more license to the licenses lis ====
        """
        assert Update_License("STORAGE", {'reason': 'Update'}, add_lic=True)
    
    @pytest.mark.testrail(id=1220599)
    @pytest.mark.Regression
    def test_GTS_lock(self):
        """
        ===== Locking the device using AOP ====
        """
        assert Update_License("STORAGE", {'reason': 'GT_lock'})
    
    @pytest.mark.testrail(id=1220600)
    @pytest.mark.Regression
    def test_GTS_unlock(self):
        """
        ===== Unocking the device using AOP ====
        """
        assert Update_License("STORAGE", {'reason': 'GT_unlock'})
    
    
