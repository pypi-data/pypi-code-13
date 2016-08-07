#!/usr/bin/python
import net_evi_agent.model.classes

def getReqFromController():
	task=classes.Compute()
	task.receive()

getReqFromController()
