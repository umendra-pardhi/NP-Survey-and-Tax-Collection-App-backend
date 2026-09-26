-- DROP SCHEMA dbo;

CREATE SCHEMA dbo;
-- demo_nagar.dbo.Accounts definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.Accounts;

CREATE TABLE Accounts ( ACID bigint IDENTITY(1,1) NOT NULL, ClientID int NULL, LedgerID int NULL, ZID int NULL, WardNo int NULL, PropertyNo int NULL, PartNo int NULL, CitySurveyNo nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, PlotNo nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, O_OnlineNo nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, O_ZID int NULL, O_WardNo int NULL, O_PropertyNo nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, O_PartNo nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, O_CitySurveyNo nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, O_PlotNo nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, O_Usage nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, O_TaxableValue float NULL, O_AnualRentalValue float NULL, Aadhar_No nvarchar(12) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, CTID int NULL, PUID int NULL, O_TotalTax decimal(18,2) NULL, Owner_Name nvarchar(500) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, Holder_Name nvarchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, Wife_Name nvarchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, BuildingName nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, BuildingNo nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, Address nvarchar(150) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, MobileNo nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, Exchange nvarchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, HasToilet bit NULL, ToiletSeats1 tinyint NULL, ToiletSeats2 tinyint NULL, HasWaterConnection bit NULL, TotalWaterConnections tinyint NULL, HasSolarElectricity bit NULL, HasRainWaterHarvesting bit NULL, HasTree bit NULL, Boundry_East nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, Boundry_West nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, Boundry_North nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, Boundry_South nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, LengthOnEast float NULL, LengthOnWest float NULL, LengthOnNorth float NULL, LengthOnSouth float NULL, Avg_Length float NULL, Avg_Breadth float NULL, Area float NULL, OPA float NULL, Gharkul bit DEFAULT 0 NULL, HasGharkul bit DEFAULT 0 NULL, TreeNos int DEFAULT 0 NULL, HasTenant bit DEFAULT 0 NULL, HasBore bit DEFAULT 0 NULL, HasWell bit DEFAULT 0 NULL, TenantName nvarchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, PhotoPath nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, MapPath nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, [Length] float DEFAULT 0 NULL, Breadth float DEFAULT 0 NULL, AsmComplete bit DEFAULT 0 NOT NULL, oldbuiltuparea float DEFAULT 0 NULL, Remark1 nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, Remark2 nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, HasTower bit DEFAULT 0 NULL, ManualRatableValue bit DEFAULT 0 NULL, ManualTax bit DEFAULT 0 NULL, Remarks3 nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, NumberingRemarks nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, NumberingDone bit NULL, SurveyDone bit NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL, CONSTRAINT PK_Accounts PRIMARY KEY (ACID));


-- demo_nagar.dbo.AssessedTax definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.AssessedTax;

CREATE TABLE AssessedTax ( ACID bigint NULL, TaxID int NULL, Amount float NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL);


-- demo_nagar.dbo.AssessedTaxCapital definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.AssessedTaxCapital;

CREATE TABLE AssessedTaxCapital ( ACID bigint NULL, TaxID int NULL, Amount float NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL);


-- demo_nagar.dbo.AssessedTaxCapitalDetails definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.AssessedTaxCapitalDetails;

CREATE TABLE AssessedTaxCapitalDetails ( ACID bigint NULL, PropertyDescription nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, PDID int NULL, TAXID int NULL, AMOUNT int DEFAULT 0 NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL);


-- demo_nagar.dbo.AssessedTaxRent definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.AssessedTaxRent;

CREATE TABLE AssessedTaxRent ( ACID bigint NULL, TaxID int NULL, Amount float NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL);


-- demo_nagar.dbo.AssessedTaxRentDetails definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.AssessedTaxRentDetails;

CREATE TABLE AssessedTaxRentDetails ( ACID bigint NULL, PropertyDescription nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, PDID int NULL, TAXID int NULL, AMOUNT int DEFAULT 0 NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL);


-- demo_nagar.dbo.Assessment definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.Assessment;

CREATE TABLE Assessment ( ASID bigint IDENTITY(1,1) NOT NULL, ACID bigint NULL, PropertyDescription nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, Floor nvarchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, con_year int NULL, con_type nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, prop_use nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, areaft float NULL, areamt float NULL, ratesqmt float NULL, monthly_rent float NULL, annual_rent float NULL, annual_tax_value float NULL, dep_per float NULL, dep_amt float NULL, gap float NULL, ff float NULL, weightage float NULL, taxable_amt float NULL, zone_point float NULL, PDID int NULL, CTID int NULL, PUID int NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL, CONSTRAINT PK_Assessment PRIMARY KEY (ASID));


-- demo_nagar.dbo.AssessmentCapital definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.AssessmentCapital;

CREATE TABLE AssessmentCapital ( ACID bigint NULL, PropertyDescription nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, floor nvarchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, con_year int NULL, ass_year int NULL, con_type nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, prop_use nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, areaft float NULL, areamt float NULL, ratesqmt float NULL, monthly_rent float NULL, annual_rent float NULL, annual_tax_value float NULL, dep_per float NULL, dep_amt float NULL, gap float NULL, ff float NULL, weightage float NULL, taxable_amt float NULL, zone_point float NULL, PDID int NULL, CTID int NULL, PUID int NULL, rep_per float DEFAULT 0 NULL, rep_amt int DEFAULT 0 NULL, ManualRatableValue bit DEFAULT 0 NULL, srnid int DEFAULT 0 NULL, buildingno nvarchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, Holder nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL);


-- demo_nagar.dbo.AssessmentRent definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.AssessmentRent;

CREATE TABLE AssessmentRent ( ACID bigint NULL, PropertyDescription nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, floor nvarchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, con_year int NULL, ass_year int NULL, con_type nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, prop_use nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, areaft float NULL, areamt float NULL, ratesqmt float NULL, monthly_rent float NULL, annual_rent float NULL, annual_tax_value float NULL, dep_per float NULL, dep_amt float NULL, gap float NULL, ff float NULL, weightage float NULL, taxable_amt float NULL, zone_point float NULL, PDID int NULL, CTID int NULL, PUID int NULL, SrNo int NULL, SRNID int NULL, rep_per float DEFAULT 0 NULL, rep_amt int DEFAULT 0 NULL, ManualRatableValue bit DEFAULT 0 NULL, buildingno nvarchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, Holder nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL);


-- demo_nagar.dbo.Capital_DepRateOnCT definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.Capital_DepRateOnCT;

CREATE TABLE Capital_DepRateOnCT ( DepID int IDENTITY(1,1) NOT NULL, ClientID int NULL, MinYear int NULL, MaxYear int NULL, CTID int NULL, ZID int NULL, Per float NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL, CONSTRAINT PK_Depreciation PRIMARY KEY (DepID));


-- demo_nagar.dbo.CarpetAreas definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.CarpetAreas;

CREATE TABLE CarpetAreas ( ACID bigint NULL, PropID int NULL, CarID int NULL, [Length] float NULL, Breadth float NULL, Area float NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL);


-- demo_nagar.dbo.Clients definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.Clients;

CREATE TABLE Clients ( ClientID int IDENTITY(1,1) NOT NULL, ClientName nvarchar(255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, ClientType nvarchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, TalukaID int NULL, DistID int NULL, StateID int NULL, Pincode nchar(6) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, MobileNo nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, PhoneNo nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, Remarks nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, ChangeBuildArea bit NULL, AskBoundry bit NULL, ValuationMethod tinyint NULL, TaxValueByAmtOrPer bit NULL, Start_year int NULL, End_year int NULL, Sign1Auth nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, Sign2Auth nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, Sign3Auth nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, Sign1 image NULL, Sign2 image NULL, Sign3 image NULL, Logo image NULL, SeparateWaterTax bit DEFAULT 0 NULL, TaxOnArea int DEFAULT 0 NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL, CONSTRAINT PK_Clients PRIMARY KEY (ClientID));


-- demo_nagar.dbo.ConstructionTypes definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.ConstructionTypes;

CREATE TABLE ConstructionTypes ( CTID int IDENTITY(1,1) NOT NULL, ConstructionType nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL, CONSTRAINT PK_ConstructionTypes PRIMARY KEY (CTID));


-- demo_nagar.dbo.DefaultLedgers definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.DefaultLedgers;

CREATE TABLE DefaultLedgers ( DLID int IDENTITY(1,1) NOT NULL, LedgerIdentity nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, LedgerID int NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL, CONSTRAINT PK_DefaultLedgers PRIMARY KEY (DLID));


-- demo_nagar.dbo.DemandTemplate definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.DemandTemplate;

CREATE TABLE DemandTemplate ( TempID int IDENTITY(1,1) NOT NULL, OrderNo int DEFAULT 0 NULL, TaxID int DEFAULT 0 NULL, LedgerID int DEFAULT 0 NULL, ItemType varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, Heading nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, [Attribute] varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, [Range] varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, Expression varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL, CONSTRAINT PK_DemandTemplate PRIMARY KEY (TempID));


-- demo_nagar.dbo.Districts definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.Districts;

CREATE TABLE Districts ( DistID int IDENTITY(1,1) NOT NULL, DistrictName nvarchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, StateID int NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL, CONSTRAINT PK_Districts PRIMARY KEY (DistID));


-- demo_nagar.dbo.EduTaxRates definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.EduTaxRates;

CREATE TABLE EduTaxRates ( RangeFrom int NULL, RangeTo int NULL, Per1 float NULL, Per2 float NULL, TaxID int NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL);


-- demo_nagar.dbo.EmpTaxRates definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.EmpTaxRates;

CREATE TABLE EmpTaxRates ( RangeFrom int NULL, RangeTo int NULL, Per float NULL, TaxID int NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL);


-- demo_nagar.dbo.FinancialYears definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.FinancialYears;

CREATE TABLE FinancialYears ( FYID int IDENTITY(1,1) NOT NULL, YearFrom int NULL, YearTo int NULL, Selected bit NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL, CONSTRAINT PK_FinancialYear PRIMARY KEY (FYID));


-- demo_nagar.dbo.FloorFactor definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.FloorFactor;

CREATE TABLE FloorFactor ( FLRID int IDENTITY(1,1) NOT NULL, ClientID int NULL, ZID int NULL, Floor nvarchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, Factor float NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL, CONSTRAINT PK_FloorFactor PRIMARY KEY (FLRID));


-- demo_nagar.dbo.LGIS definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.LGIS;

CREATE TABLE LGIS ( LGIID int IDENTITY(1,1) NOT NULL, InstituteTypeName nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL, CONSTRAINT PK_LGIS PRIMARY KEY (LGIID));


-- demo_nagar.dbo.LedgerTypes definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.LedgerTypes;

CREATE TABLE LedgerTypes ( LTID tinyint NULL, LedgerType nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL);


-- demo_nagar.dbo.Ledgers definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.Ledgers;

CREATE TABLE Ledgers ( LedgerID int IDENTITY(1,1) NOT NULL, LedgerName nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, LedgerType tinyint NULL, ClientID int NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL, CONSTRAINT PK_Ledgers PRIMARY KEY (LedgerID));


-- demo_nagar.dbo.PhotosMaps definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.PhotosMaps;

CREATE TABLE PhotosMaps ( ClientID int NULL, ACID bigint NOT NULL, Photo image NULL, [Map] image NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL);


-- demo_nagar.dbo.PropertyDesc definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.PropertyDesc;

CREATE TABLE PropertyDesc ( PDID int IDENTITY(1,1) NOT NULL, PropertyDescription nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, Weightage float DEFAULT 0.0 NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL, CONSTRAINT PK_PropertyDesc PRIMARY KEY (PDID));


-- demo_nagar.dbo.PropertyUsage definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.PropertyUsage;

CREATE TABLE PropertyUsage ( PUID int IDENTITY(1,1) NOT NULL, PropertyUse nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, PDID int NULL, TaxAmount int DEFAULT 0 NULL, GWTax int DEFAULT 0 NULL, SWTax int DEFAULT 0 NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL, CONSTRAINT PK_PropertyHeads PRIMARY KEY (PUID));


-- demo_nagar.dbo.PropertyUsageOld definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.PropertyUsageOld;

CREATE TABLE PropertyUsageOld ( PUID int IDENTITY(1,1) NOT NULL, PropertyUse nvarchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL, CONSTRAINT PK_PropertyUsageOld PRIMARY KEY (PUID));


-- demo_nagar.dbo.RECOUNT definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.RECOUNT;

CREATE TABLE RECOUNT ( RID int NULL, RType varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, FYID int NULL, RECNO int NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL);


-- demo_nagar.dbo.RateOnCTZonewise_Capital definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.RateOnCTZonewise_Capital;

CREATE TABLE RateOnCTZonewise_Capital ( CTZRID int IDENTITY(1,1) NOT NULL, ClientID int NULL, ZID int NULL, CTID int NULL, Rate int NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL, CONSTRAINT PK_RateOnCTZonewise PRIMARY KEY (CTZRID));


-- demo_nagar.dbo.RateOnCTZonewise_Rent definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.RateOnCTZonewise_Rent;

CREATE TABLE RateOnCTZonewise_Rent ( CTZRID int IDENTITY(1,1) NOT NULL, ClientID int NULL, ZID int NULL, CTID int NULL, Rate int NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL, CONSTRAINT PK_RateOnCTZonewise_Rent PRIMARY KEY (CTZRID));


-- demo_nagar.dbo.ReceiptTemplate definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.ReceiptTemplate;

CREATE TABLE ReceiptTemplate ( TempID int IDENTITY(1,1) NOT NULL, OrderNo int DEFAULT 0 NULL, TaxID int DEFAULT 0 NULL, LedgerID int DEFAULT 0 NULL, ItemType varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, Heading nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, [Attribute] varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, [Range] varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, Expression varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL, CONSTRAINT PK_ReceiptTemplate PRIMARY KEY (TempID));


-- demo_nagar.dbo.Rent_DepRateOnCT definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.Rent_DepRateOnCT;

CREATE TABLE Rent_DepRateOnCT ( DepID int IDENTITY(1,1) NOT NULL, ClientID int NULL, MinYear int NULL, MaxYear int NULL, CTID int NULL, Per float NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL, CONSTRAINT PK_Rent_DepRateOnCT PRIMARY KEY (DepID));


-- demo_nagar.dbo.Rent_RepairingRateOnCT definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.Rent_RepairingRateOnCT;

CREATE TABLE Rent_RepairingRateOnCT ( RepID int IDENTITY(1,1) NOT NULL, ClientID int NULL, MinYear int NULL, MaxYear int NULL, CTID int NULL, Per float NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL, CONSTRAINT PK_Rent_RepRateOnCT PRIMARY KEY (RepID));


-- demo_nagar.dbo.Settings definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.Settings;

CREATE TABLE Settings ( SettingName nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, StringValue nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, IntegerValue int NULL, FloatValue float NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL);


-- demo_nagar.dbo.States definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.States;

CREATE TABLE States ( StateID int IDENTITY(1,1) NOT NULL, StateName nvarchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL, CONSTRAINT PK_States PRIMARY KEY (StateID));


-- demo_nagar.dbo.TaxDemandPaymentDetails definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.TaxDemandPaymentDetails;

CREATE TABLE TaxDemandPaymentDetails ( DID bigint NULL, TaxID int NULL, PreviousBalance int DEFAULT 0 NULL, CurrentBalance int DEFAULT 0 NULL, PreviousPaid int DEFAULT 0 NULL, CurrentPaid int DEFAULT 0 NULL, RemPreviousBalance int DEFAULT 0 NULL, RemCurrentBalance int DEFAULT 0 NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL);


-- demo_nagar.dbo.TaxDemands definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.TaxDemands;

CREATE TABLE TaxDemands ( DID bigint IDENTITY(1,1) NOT NULL, RECNO bigint NOT NULL, ACID bigint NULL, DDate date NULL, FYID int NULL, SumPrevious int NULL, SumNew int NULL, SumTotal int NULL, ExAdjustment int NULL, Advance int NULL, Adjustment int NULL, Discount int NULL, TotalPayableAmt int NULL, InWords nvarchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, DPAID tinyint NULL, TranID bigint NULL, WaterTax float NULL, MainDemand bit DEFAULT 0 NOT NULL, locked bit DEFAULT 0 NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL, CONSTRAINT PK_TaxDemand PRIMARY KEY (DID));


-- demo_nagar.dbo.TaxPaymentDetails definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.TaxPaymentDetails;

CREATE TABLE TaxPaymentDetails ( PYID bigint NULL, DID bigint NULL, TaxID int NULL, LedgerID bigint NULL, BalancePaid float NULL, CurrentPaid float NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL);


-- demo_nagar.dbo.TaxPayments definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.TaxPayments;

CREATE TABLE TaxPayments ( PYID bigint IDENTITY(1,1) NOT NULL, DID bigint NULL, RECNO bigint NULL, ACID bigint NULL, DDate datetime NULL, FYID int NULL, SumPrevious float NULL, SumCurrent float NULL, ExAdjustment float NULL, Advance float NULL, Discount float NULL, CashDiscount float NULL, BalanceAmt float NULL, ExcessAmt float NULL, WaterTax float NULL, TotalBillAmt float NULL, TotalPayableAmt float NULL, AmountPaid float NULL, InWords nvarchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, PaymentMode nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, InstrumentNo nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, InstrumentDate date NULL, BankName nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, Receiver nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, ReceivedFrom nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, TRANID bigint NULL, Penalty float NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL, CONSTRAINT PK_TaxPayment PRIMARY KEY (PYID));


-- demo_nagar.dbo.TaxRates definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.TaxRates;

CREATE TABLE TaxRates ( MinArea int NULL, MaxArea int NULL, Amount float NULL, Per float NULL, TSRate1 int DEFAULT 0 NULL, TSRate2 int DEFAULT 0 NULL, TaxID int NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL);


-- demo_nagar.dbo.TaxTypes definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.TaxTypes;

CREATE TABLE TaxTypes ( TaxID int IDENTITY(1,1) NOT NULL, TaxType nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, TaxOverToiletSeat bit DEFAULT 0 NULL, TaxOnWaterConnection bit NULL, TaxOnWholeProperty bit NULL, EducationTax bit NULL, EmploymentTax bit NULL, UsageTax bit DEFAULT 0 NULL, PropertyTax bit DEFAULT 0 NULL, FireSafetyTax bit DEFAULT 0 NULL, AdvtTax bit DEFAULT 0 NULL, SpecialTax bit DEFAULT 0 NULL, OrdNo int NULL, fix bit NULL, ValuedOn int NULL, LedgerID int NULL, OldTax bit DEFAULT 0 NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL, CONSTRAINT PK_TaxTypes PRIMARY KEY (TaxID));


-- demo_nagar.dbo.Taxprodeal definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.Taxprodeal;

CREATE TABLE Taxprodeal ( PDID int NULL, TaxID int NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL);


-- demo_nagar.dbo.TowerTaxPer definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.TowerTaxPer;

CREATE TABLE TowerTaxPer ( ID int NULL, TowerPer int NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL);


-- demo_nagar.dbo.Transactions definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.Transactions;

CREATE TABLE Transactions ( TranID bigint IDENTITY(1,1) NOT NULL, FYID int NULL, TranDate datetime NULL, VoucherType tinyint NULL, VoucherNo int NULL, TranDetails nvarchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, Remarks nvarchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, Amount float NULL, UserID int NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL, CONSTRAINT PK_Transactions PRIMARY KEY (TranID));


-- demo_nagar.dbo.UsageLog definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.UsageLog;

CREATE TABLE UsageLog ( LogID bigint IDENTITY(1,1) NOT NULL, LogType varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, Description nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, LogDate datetime NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL, CONSTRAINT PK_UsageLog PRIMARY KEY (LogID));


-- demo_nagar.dbo.Users definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.Users;

CREATE TABLE Users ( UserID int IDENTITY(1,1) NOT NULL, UserName nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, Mobile nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, DOB date NULL, EMail nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, LoginID nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, Password nvarchar(255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, UserRole nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, UserLocation bit NULL, ClientID int NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL, CONSTRAINT PK_Users PRIMARY KEY (UserID));


-- demo_nagar.dbo.VMValue definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.VMValue;

CREATE TABLE VMValue ( VMID int NOT NULL, ValuedOn nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL, CONSTRAINT PK_VMValue PRIMARY KEY (VMID));


-- demo_nagar.dbo.WaterConnections definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.WaterConnections;

CREATE TABLE WaterConnections ( ACID bigint NULL, Owner_Name nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, Pipe_Size nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, size_value int NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL);


-- demo_nagar.dbo.Weightages definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.Weightages;

CREATE TABLE Weightages ( ZID int NULL, PTID int NULL, Weightage float NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL);


-- demo_nagar.dbo.Zones definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.Zones;

CREATE TABLE Zones ( ZID int IDENTITY(1,1) NOT NULL, ZoneName nvarchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, PointsPer float DEFAULT 0.0 NULL, ClientID int NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL, CONSTRAINT PK_Zones PRIMARY KEY (ZID));


-- demo_nagar.dbo.AccountsPhotos definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.AccountsPhotos;

CREATE TABLE AccountsPhotos ( ImageId int IDENTITY(1,1) NOT NULL, ACID bigint NOT NULL, FileName varchar(255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, MimeType varchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, ImagePath varchar(500) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL, CONSTRAINT PK__Accounts__7516F70C889A2488 PRIMARY KEY (ImageId), CONSTRAINT FK__AccountsPh__ACID__5B438874 FOREIGN KEY (ACID) REFERENCES Accounts(ACID));


-- demo_nagar.dbo.Talukas definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.Talukas;

CREATE TABLE Talukas ( TalukaID int IDENTITY(1,1) NOT NULL, TalukaName nvarchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, DistID int NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL, CONSTRAINT PK_Talukas PRIMARY KEY (TalukaID), CONSTRAINT FK_Talukas_Districts FOREIGN KEY (DistID) REFERENCES Districts(DistID));


-- demo_nagar.dbo.TaxDemandDetails definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.TaxDemandDetails;

CREATE TABLE TaxDemandDetails ( DID bigint NULL, TaxID int NULL, PreviousBalance float NULL, CurrentBalance float NULL, TotalBalance float NULL, LedgerID bigint NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL, CONSTRAINT FK_TaxDemandDetails_TaxDemands FOREIGN KEY (DID) REFERENCES TaxDemands(DID) ON DELETE CASCADE);


-- demo_nagar.dbo.TransactionDetails definition

-- Drop table

-- DROP TABLE demo_nagar.dbo.TransactionDetails;

CREATE TABLE TransactionDetails ( TranID bigint NULL, SN tinyint NULL, LedgerID1 bigint NULL, LedgerID2 bigint NULL, Debit decimal(12,2) NULL, Credit decimal(12,2) NULL, DrCr nchar(2) COLLATE SQL_Latin1_General_CP1_CI_AS NULL, created_at datetime DEFAULT getdate() NULL, updated_at datetime DEFAULT getdate() NULL, deleted_at datetime NULL, sync_version bigint DEFAULT 1 NULL, CONSTRAINT FK_TransactionDetails_Transactions FOREIGN KEY (TranID) REFERENCES Transactions(TranID) ON DELETE CASCADE);