import { ComfyApp, app } from "../../scripts/app.js"
import { api } from "../../scripts/api.js";


function debounce(func, wait) {
    let timeout;

    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };

        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

const debounce_update_url_settings = debounce(update_settings, 1000);
const debounce_update_bucket_settings = debounce(update_settings, 1000);
const debounce_update_access_settings = debounce(update_settings, 1000);
const debounce_update_secret_settings = debounce(update_settings, 1000);

async function update_settings(setting, value) {
    console.log(`Setting ${setting}: ${value}`);
    const data = {}
    data[setting] = value;
    const resp = await api.fetchApi(`/saveimages3/setting/${setting}`, {
        method: 'PATCH',
        body: JSON.stringify(data),
        cache: 'no-store',
      });
      if (resp.status === 200) {
        return await resp.text();
      }
      throw new Error(resp.statusText);
}

class SaveImageS3Plugin
{
    extentionName = "Chipset.SaveImageS3";

    createSettingsURL = () => {
        this.settingsURL = {
            id: "Chipset.SaveImageS3.URL",
            type: "string",
            name: "S3 URL",
            category: ['SaveImageS3', 'Configuration', 'url'],
            tooltip: 'S3 URL',
            type: "text",
            defaultValue: "",
            onChange: (value) => {
                debounce_update_url_settings("url", value);
            }
        }
    }

    createSettingsAccessKey = () => {
        this.settingsAccessKey = {
            id: plugin.extentionName + ".AccessKey",
            type: "string",
            name: "Access Key",
            category: ['SaveImageS3', 'Configuration', 'access'],
            tooltip: 'Access Key',
            type: "text",
            defaultValue: "",
            onChange: (value) => {
                debounce_update_access_settings('access', value);
            }
        }
    }

    createSettingsSecretKey = () => {
        this.settingsSecretKey = {
            id: plugin.extentionName + ".SecretKey",
            type: "string",
            name: "Secret Key",
            category: ['SaveImageS3', 'Configuration', 'secret'],
            tooltip: 'Secret Key',
            type: "text",
            defaultValue: "",
            onChange: (value) => {
                debounce_update_secret_settings('secret', value);
            }
        }
    }

    createSettingsBucketName = () => {
        this.settingsBucketName = {
            id: plugin.extentionName + ".BucketName",
            type: "string",
            name: "Bucket Name",
            category: ['SaveImageS3', 'Configuration', 'bucket'],
            tooltip: 'Bucket Name',
            type:  "text",
            defaultValue: "",
            onChange: (value) => {
                debounce_update_bucket_settings('bucket', value);
            }
        }
    }

    addSettingsUI = () => {
        app.ui.settings.addSetting(this.settingsSecretKey);
        app.ui.settings.addSetting(this.settingsAccessKey);
        app.ui.settings.addSetting(this.settingsBucketName);
        app.ui.settings.addSetting(this.settingsURL);

    }

}

const plugin = new SaveImageS3Plugin();

app.registerExtension({
    name: plugin.extentionName,
    async setup() {
        console.log("Comfy.SaveImageS3 setup!!!");
        plugin.createSettingsURL();
        plugin.createSettingsAccessKey();
        plugin.createSettingsSecretKey();
        plugin.createSettingsBucketName();

        plugin.addSettingsUI();
    },
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        // console.log(nodeType.comfyClass);
        if (nodeType.comfyClass=="SaveImageS3") { 
            console.log("SaveImageS3 node is registed")
        }
    }
})

