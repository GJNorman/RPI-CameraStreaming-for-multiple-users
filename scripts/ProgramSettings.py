#this file is overwritten programmatically; don't add any data outside of this dictionary
#all dictionary keys must be strings
global_Settings = {
	"ModuleType":"ApplicationTestModule",
	"ModuleName":"Camera1",
	"Camera_Horizontal_Resolution":1280,
	"Camera_Vertical_Resolution":720,
	"Camera_Scale_pxls_per_mm":1.0,
	"Camera_FPS":30,
	"Camera_Export_As_Gray":False,
	"Camera_ROI_List":{
		"EXAMPLE_ROI_1":[[40,40],[60,60],"orange"],
		"EXAMPLE_ROI_2":[[10,15],[20,40],"blue"],
	},
        "SOCKET_FRAMES_TO_BUFFER":1,
	"SOCKET_liveStream":"tcp://*:5555",
	"SOCKET_HeartBeat":"tcp://*:5556",
	"SOCKET_ArchiveStream":"tcp://*:5557",
	"SOCKET_WebInterfaceIO":"tcp://*:5558",
	}
