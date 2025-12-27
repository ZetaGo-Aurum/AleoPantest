from aleopantest.core.base_tool import BaseTool, ToolMetadata, ToolCategory

class CronGen(BaseTool):
    def __init__(self):
        metadata = ToolMetadata(
            name="Cron Expression Generator",
            category=ToolCategory.UTILITIES,
            version="1.0.0",
            author="deltaastra24@gmail.com",
            description="Membuat ekspresi cron untuk jadwal tugas otomatis",
            usage="aleopantest run cron-gen --minute <m> --hour <h>",
            example="aleopantest run cron-gen --minute 0 --hour 12",
            parameters={
                "minute": "Menit (0-59)",
                "hour": "Jam (0-23)",
                "dom": "Day of Month (1-31)",
                "month": "Bulan (1-12)",
                "dow": "Day of Week (0-6)"
            },
            requirements=[],
            tags=["utility", "cron", "automation"]
        )
        super().__init__(metadata)

    def run(self, minute="*", hour="*", dom="*", month="*", dow="*", **kwargs):
        expression = f"{minute} {hour} {dom} {month} {dow}"
        return {"expression": expression, "explanation": f"Tugas akan berjalan pada menit {minute}, jam {hour}, hari {dom}, bulan {month}, dan hari ke-{dow}."}

    def validate_input(self, **kwargs) -> bool: return True
