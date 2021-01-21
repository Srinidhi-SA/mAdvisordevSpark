import store from "../store";
import {isEmpty} from "../helpers/helper";

export function openCreateSignalModal() {
		 return {
				type: "CREATE_SIGNAL_SHOW_MODAL",
			}
	}

	export function closeCreateSignalModal() {
		return {
			type: "CREATE_SIGNAL_HIDE_MODAL",
		}
	}

	export function openCsLoaderModal() {
		return {
			type: "SHOW_CREATE_SIGNAL_LOADER",
		}
	}

	export function closeCsLoaderModal() {
		return {
			type: "HIDE_CREATE_SIGNAL_LOADER",
		}
	}

	export function updateCsLoaderValue(value) {
		return {
			type: "CREATE_SIGNAL_LOADER_VALUE",
			value
		}
	}

	export function updateCsLoaderMsg(message) {
	  return {type: "CREATE_SIGNAL_LOADER_MSG", message}
	}
