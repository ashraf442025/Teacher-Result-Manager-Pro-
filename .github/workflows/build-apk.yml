name: Build Teacher Result Manager Pro APK

on:
  workflow_dispatch:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-22.04

    steps:

      # ==========================================================
      # 1. CHECKOUT
      # ==========================================================
      - name: Checkout repository
        uses: actions/checkout@v4


      # ==========================================================
      # 2. JAVA 17
      # ==========================================================
      - name: Setup Java 17
        uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: '17'


      # ==========================================================
      # 3. PYTHON 3.11
      # ==========================================================
      - name: Setup Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'


      # ==========================================================
      # 4. ANDROID SDK
      # IMPORTANT:
      # DO NOT REQUEST "tools"
      # ==========================================================
      - name: Setup Android SDK
        uses: android-actions/setup-android@v4
        with:
          packages: 'platform-tools'


      # ==========================================================
      # 5. ACCEPT SDK LICENSES
      # ==========================================================
      - name: Accept Android SDK licenses
        shell: bash
        run: |
          set +e

          yes | sdkmanager --licenses

          exit 0


      # ==========================================================
      # 6. INSTALL REQUIRED SDK PACKAGES
      # ==========================================================
      - name: Install Android SDK packages
        shell: bash
        run: |
          set -eux

          sdkmanager \
            "platform-tools" \
            "platforms;android-35" \
            "build-tools;35.0.0"

          yes | sdkmanager --licenses || true


      # ==========================================================
      # 7. VERIFY SDK
      # ==========================================================
      - name: Verify Android SDK
        shell: bash
        run: |
          set -eux

          echo "ANDROID_HOME=$ANDROID_HOME"
          echo "ANDROID_SDK_ROOT=$ANDROID_SDK_ROOT"

          echo ""
          echo "Installed Build Tools:"
          ls -la "$ANDROID_HOME/build-tools"

          echo ""
          echo "Checking AIDL..."

          test -f "$ANDROID_HOME/build-tools/35.0.0/aidl"

          "$ANDROID_HOME/build-tools/35.0.0/aidl" --version || true

          echo ""
          echo "AIDL FOUND SUCCESSFULLY"


      # ==========================================================
      # 8. INSTALL BUILD DEPENDENCIES
      # ==========================================================
      - name: Install Python build dependencies
        shell: bash
        run: |
          python -m pip install --upgrade pip
          python -m pip install --upgrade setuptools wheel
          python -m pip install --upgrade buildozer


      # ==========================================================
      # 9. CLEAN BUILD
      # ==========================================================
      - name: Clean Buildozer
        shell: bash
        run: |
          buildozer android clean || true


      # ==========================================================
      # 10. BUILD APK
      # ==========================================================
      - name: Build APK
        shell: bash
        env:
          ANDROID_HOME: ${{ env.ANDROID_HOME }}
          ANDROID_SDK_ROOT: ${{ env.ANDROID_HOME }}
        run: |
          set -o pipefail

          echo "Final Android SDK check..."

          test -f "$ANDROID_HOME/build-tools/35.0.0/aidl"

          echo "Starting Buildozer..."

          buildozer -v android debug


      # ==========================================================
      # 11. UPLOAD APK
      # ==========================================================
      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: Teacher-Result-Manager-Pro-APK
          path: bin/*.apk
          if-no-files-found: error
