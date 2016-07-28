# Generated with django-for-android

#App
--name="{{APK_NAME}}"
--version={{VERSION}}
--package={{PACKAGE}}
--private=app
--icon={{ICON}}
--orientation={{ORIENTATION}}

#Permissions
{{PERMISSIONS}}

#Custom directories
--storage-dir={{BUILD_DIR}}
--local-recipes={{RECIPES_DIR}}

#Project features
--requirements={{REQUIREMENTS}}
--bootstrap=djangoview
--port={{PORT}}

#SDK options
--sdk_dir={{ANDROID_SDK}}
--android_api={{ANDROID_SDK_API}}

#NDK options
--ndk_dir={{CRYSTAX_NDK}}
--ndk_ver={{CRYSTAX_NDK_VERSION}}

#Other options
--arch={{ARCH}}
--dist_name=djangoserver
#--whitelist={{WHITELIST}}
