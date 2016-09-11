#!/usr/bin/env python
import rpyc
import tempfile
import os
import time
# import modelagem
from AutomodelServerModules.file import *
import zipfile
from modellerstep.Mold import mold
from modellerstep.Modeller import Modeler
from modellerstep.Align import Align
from modellerstep.Malign import Malign
from modellerstep.Malign2 import Malign2
from modellerstep.MakeProfile import MakeProfile
from modellerstep.GetProt2 import GetProt2
from modellerstep.GetProt import GetProt
from modellerstep.Procheck_Evaluate import Procheck_Evaluate
from modellerstep.Loop_Refinement import Loop_Refinement
from modellerstep.GetDataFromPDB import GetDataFromPDB



# PDBFolder = "/home/jorgehf/PDB/"
# PDBFolder = "/home/joao/Projeto/pdb/"
PFAMDatabase = "/home/jorgehf/Pfam-A.hmm"


class ServerService(rpyc.Service):
	"""docstring for ServerService"""
	def __init__(self, arg):
		# super(ServerService, self).__init__()
		self.arg = arg
		self.workdir = tempfile.mkdtemp() + "/"
		print self.workdir
		self.pdb_folder = self.workdir

	def exposed_receive_file(self, filename):
		# time.sleep(2)
		return open(self.workdir + os.path.basename(filename), "r")

	def exposed_check_serial(self, password):
		if password == "MODELIRANJE":
			return True
		else:
			return False

	def exposed_receive_file(self, filename, buffer_file):
		received_file = file(self.workdir + os.path.basename(filename), "w")
		received_file.write(buffer_file)
		received_file.close()

	def exposed_find_templates(self,serial):
		# self.callback = rpyc.async(callback)
		teste = mold(self.workdir + "seq.ali")
		teste.make_build_profilepy()
		teste.find_templates()
		# self.callback("find_templates")

	def exposed_send_file(self, name_of_file):
		sending_file = file(self.workdir + os.path.basename(name_of_file), "r")
		buffer_file = sending_file.load_in_memory()
		sending_file.close()
		return buffer_file

	def exposed_send_template(self, pdb_name):
		template_manager = GetDataFromPDB(self.workdir, pdb_name)
		pdb_path = template_manager.getPDB_File()

		# pdb_path = self.pdb_folder + pdb_name + ".pdb"
		sending_file = file(pdb_path, "r")
		buffer_file = sending_file.load_in_memory()
		sending_file.close()
		return buffer_file

	def exposed_align(self,pir_sequence_file,template):
			# template_manager = GetDataFromPDB(workdir, better_profile.name())
			# downloaded_pdb_path = template_manager.getPDB_File()
			# downloaded_pdb = PDBFile(downloaded_pdb_path,'r')
			teste = Align(self.workdir, os.path.basename(template),os.path.basename(pir_sequence_file))
			teste.convert_seqali_pir_to_fasta_formar()
	#		teste.search_an_hmmm()
	#		teste.find_better_motif()
	#		teste.fetch_the_hmm()
	#		teste.align_with_hmmer()
			teste.align_with_muscle()
			teste.convert_fasta_to_pir()

		

		# return os.path.basename(best_result)
		# teste.align()

	def exposed_model(self, ali_ali, template):
		teste = Modeler( self.workdir, os.path.basename(template), os.path.basename(ali_ali))
		teste.make_get_model_py()
		teste.model_sequence()
		best_result = teste.get_results()
		# print 
		return os.path.basename(best_result)

	def exposed_evaluate(self,template,model_file,ali_ali_file):
		# teste = modelagem.Evaluate(template,model_file,ali_ali_file,self.workdir)
		# teste.make_evaluate_model(model_file)
		# teste.get_evaluate()
		# teste.make_evaluate_model(template)
		# teste.get_evaluate()
		# teste.plot_profiles()
		# return  'dope_profile.png'

		# loop_refinament_folder = self.workdir 
		evaluate_folder = self.workdir
		if not os.path.exists(evaluate_folder):
			os.mkdir(evaluate_folder)
		best_model = self.workdir + model_file
		# loop_model = self.workdir + loopmodel
		my_template = self.workdir + template
		# os.popen("cp "+ best_model + " " + loop_val)
		# os.popen("cp "+ loop_model + " " + loop_val)
		# os.popen("cp "+ my_template + " " + loop_val)
		multiple_align = Malign2(evaluate_folder)
		multiple_align.create_script_in_folder(os.path.basename(my_template)[0:-4],os.path.basename(best_model)[0:-4])
		multiple_align.get_model()
		profile_best_model = MakeProfile()
		profile_best_model.create_script_in_folder(evaluate_folder + os.path.basename(model_file))
		profile_best_model.get_model()
		profile_my_template = MakeProfile()
		profile_my_template.create_script_in_folder(evaluate_folder + os.path.basename(template))
		profile_my_template.get_model()
		# profile_loop_model = modelagem.MakeProfile()
		# profile_loop_model.create_script_in_folder(evaluate_folder + os.path.basename(loopmodel))
		# profile_loop_model.get_model()

		plot_profiles = GetProt2(evaluate_folder)
		plot_profiles.create_script_in_folder(my_template,best_model)
		plot_profiles.get_model()
		return "dope_profile_loop.png"

	def exposed_evaluatePROCHECK(self, model_file):
		teste = Procheck_Evaluate(self.workdir, model_file)
		teste.copy_templates_for_procheck_evaluate()
		procheck_folder = teste.run_prochek()
		zipped_procheck_folder_name = procheck_folder + ".zip"
		zipped_procheck_folder = self.__zipper__(procheck_folder,zipped_procheck_folder_name)
		return os.path.basename(zipped_procheck_folder)

	def __recursive_zip__(self,zipf, directory, folder = ""):
		for item in os.listdir(directory):
			if os.path.isfile(os.path.join(directory, item)):
				zipf.write(os.path.join(directory, item), folder + os.sep + item)
			elif os.path.isdir(os.path.join(directory, item)):
				self.__recursive_zip__(zipf, os.path.join(directory, item), folder + os.sep + item)

	def __zipper__(self,folder,nome_destino):
		zipz = nome_destino
		zipf = zipfile.ZipFile(zipz, "w", compression=zipfile.ZIP_DEFLATED )
		path = folder
		self.__recursive_zip__(zipf, path)
		zipf.close()
		return nome_destino

	def exposed_loopmodel(self,model, start_residue, end_residue):
		teste = Loop_Refinement(self.workdir + os.path.basename(model), start_residue, end_residue)
		teste.create_script_in_folder(self.workdir)
		teste.get_model()
		best_result = teste.get_results()
		# print 
		return os.path.basename(best_result)

	def exposed_evaluatelooprefinament(self,template,model_file,loopmodel, ali_ali_file):
   # def __loop_refinament_validation__(self,thread, callback):
		# self.callback = rpyc.async(callback)
		loop_refinament_folder = self.workdir 
		loop_val = loop_refinament_folder # + "loop_val" +loop +  os.sep
		if not os.path.exists(loop_val):
			os.mkdir(loop_val)
		best_model = self.workdir + model_file
		loop_model = self.workdir + loopmodel
		my_template = self.workdir + template
		# os.popen("cp "+ best_model + " " + loop_val)
		# os.popen("cp "+ loop_model + " " + loop_val)
		# os.popen("cp "+ my_template + " " + loop_val)
		multiple_align = Malign(loop_val)
		multiple_align.create_script_in_folder(os.path.basename(my_template)[0:-4],os.path.basename(best_model)[0:-4],os.path.basename(loop_model)[0:-4])
		multiple_align.get_model()
		profile_best_model = MakeProfile()
		profile_best_model.create_script_in_folder(loop_val + os.path.basename(model_file))
		profile_best_model.get_model()
		profile_my_template = MakeProfile()
		profile_my_template.create_script_in_folder(loop_val + os.path.basename(template))
		profile_my_template.get_model()
		profile_loop_model = MakeProfile()
		profile_loop_model.create_script_in_folder(loop_val + os.path.basename(loopmodel))
		profile_loop_model.get_model()

		plot_profiles = GetProt(loop_val)
		plot_profiles.create_script_in_folder(my_template,best_model,loop_model)
		plot_profiles.get_model()
		return "dope_profile_loop.png"

		# self.dope_profile_loop = "loop/dope_profile.png"
		# self.callback("dope_profile_loop")



if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(ServerService, port = 18861)
    t.start()
