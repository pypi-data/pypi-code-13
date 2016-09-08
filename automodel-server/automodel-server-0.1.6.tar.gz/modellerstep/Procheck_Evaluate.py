import os

class Procheck_Evaluate:
    def __init__(self,workdir,template):
        self.workdir = workdir
        self.procheck_workdir = self.prepare_folder()
        self.template = self.workdir + os.path.basename(template)
        self.template_on_procheck_folder = None
    def prepare_folder(self):
        pastadeavaliacao = self.workdir + 'avaliacao_procheck/'
        if os.path.exists(pastadeavaliacao):
	        os.popen('rm -fr '+ pastadeavaliacao)
        os.mkdir(pastadeavaliacao)
        return pastadeavaliacao

    def copy_templates_for_procheck_evaluate(self):
        os.popen('cp '+ self.template +  ' ' + self.procheck_workdir)
        self.template_on_procheck_folder = self.procheck_workdir + os.path.basename(self.template)

    def run_prochek(self):
      script = """\
import os
#path = os.getcwd()
os.chdir('""" + self.procheck_workdir + """')
os.popen('procheck '+ '""" + self.template_on_procheck_folder + """' +  ' ' + str(2.0))
#os.chdir(path)
      """
      script_path = self.procheck_workdir + "procheck.py"
      procheck_script = file(script_path, "w")        
      procheck_script.write(script)
      procheck_script.close()
      os.popen("python " + script_path)
      return self.procheck_workdir[0:-1] 