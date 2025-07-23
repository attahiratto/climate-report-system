from django.core.management.base import BaseCommand
from reports.utils.parser import run_parser
        

class Command(BaseCommand):
    
    def handle(self,*args,**kwargs):
        run_parser() 
        self.stdout.write(self.style.SUCCESS("updated records successfully"))