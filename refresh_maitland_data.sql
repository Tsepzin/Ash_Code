USE [AshburtonRisk]
GO

DECLARE       @return_value int

EXEC   @return_value = [dbo].[spImport_Maitland_ASISA_Instruments_LOOP_Month]
              @RunDate = '2020-10-31'

SELECT 'Return Value' = @return_value


EXEC   @return_value = [dbo].[spImport_Maitland_Holdings_Monthly_Portfolio_CURRENT]
              @RunDate = '2020-10-31'

SELECT 'Return Value' = @return_value

GO
