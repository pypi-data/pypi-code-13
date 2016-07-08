"""Created on September 2015

@author: AAMomin

The module assembles a protein graph based in input argunements. Further 
calulation are computed within GraphCalculation.py
"""



# Python Graphics package import 
import svgwrite
import GraphCalculation as Calc

class GraphAssemble(object):
	"""
	The class takes an input of he protein length, Coverage  and PTM/Modification site
	
	Input: arguments 'file name', 'length', 'mod position list' and 'peptide coverage coordinate'
	
	Output: Saved SVG output
 
    Example     
    
    EGFR = Asb.GraphAssemble("test_1125.svg",375)  # Create an instance of the class and provide file name and length
    EGFR.AddMolecule()                             # Add a molecule backbone of the specified length
    KnownMod = [50,84]                             # List to known mod positions
    uKnownMod = [113,238,312]                      # List of unknown mod positions
    EGFR.AddTicks(KnownMod,"circle")               # Make tics with knownmods
    EGFR.AddTicks(uKnownMod,"triangle")            # Make tics with unknownMods 
    EGFR.PrintFigure()                             # Save the SVG figure  
    
    """

	def __init__(self, filename, length_mol):
         ## Crete a drawing are for the SVG figure
         self.svg_document = svgwrite.Drawing(filename = filename,	size = ("1400px", "600px"))
         self.mol_length = length_mol
          
          
	
	def AddMolecule(self):
		## Add the protein sequenc graphic and any domain structure with color
		self.svg_document.add(self.svg_document.rect(insert = (200, 200), size = ("800px", "25px"), stroke_width = "1", stroke = "black", fill = "rgb(255,255,0)"))
		
	def AddTicks(self,Positions,shape):
		for i in range(len(Positions)):
			mutPosition = Calc.finalTickPosition(800,self.mol_length,Positions[i],200,100)
			self.svg_document.add(self.svg_document.rect(insert = (mutPosition, 180),size = ("1px", "20px"),stroke_width = "1",stroke = "red",fill = "rgb(255,255,0)"))
			if shape == "circle":
				self.svg_document.add(self.svg_document.circle(center=(mutPosition, 175),r=5,stroke_width = "1",stroke = "red",fill = "rgb(255,255,0)"))
			elif shape == "triangle":
				#mutPosition = Calc.finalTickPosition(800,1600,KnownMod[i],200,100) #print mutPosition
				originX = mutPosition - 4
				originY = 175
				self.svg_document.add(self.svg_document.polygon([(originX, originY), (originX + 8, originY - 4), (originX + 8, originY + 4)],stroke_width = "1",stroke = "blue",fill = "rgb(0,0,255)"))
			else:
				pass
				
    
	
	def AddCoverage(self,PepInterval):
		for i in range(len(PepInterval)):
			start, stop = Calc.peptideCoverageIntervals(PepInterval[i],800,self.mol_length,200,100) #topX = start
			topY = 280 			#lowerX = mutPosition - 4
			lowerY = 300        #print(start,stop)
			self.svg_document.add(self.svg_document.polygon([(start,topY),(stop,topY), (stop,lowerY), (start,lowerY)],
													stroke_width = "1",stroke = "blue",fill = "rgb(0,0,255)"))
	
	def PrintFigure(self):
		self.svg_document.save()