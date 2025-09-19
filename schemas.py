from pydantic import BaseModel, Field

class OpportunityFeatures(BaseModel):
    Industry: str
    Company_Size: str
    Contact_Title: str
    Engagement_Score: float
    Product_Interest: str
    Region: str
    Prior_Deals: str
    Is_Good_Opportunity: int
