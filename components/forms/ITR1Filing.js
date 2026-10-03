"use client";

import { useState } from "react";
import { SparklesIcon } from "../Icons";
import DocumentUploadCard from "../DocumentUploadCard";
import OutputJsonViewer from "../OutputJsonViewer";
import { generateItr1Json } from "@/libs/forms/itr1JsonGenerator";
import { downloadJson } from "@/libs/downloadHelper";
import { parseTaxFile } from "@/utils/taxFileParser";
import {
  INITIAL_PROFILE,
  INITIAL_ADDRESS,
  INITIAL_BANK,
  INITIAL_VERIFICATION
} from "./common/constants";
import { mergeTaxpayerData } from "@/utils/prefillParser";
import ITRPrefillDetails from "./common/ITRPrefillDetails";
import { parsePanImageClient } from "@/utils/panExtractor";
import { parseAadhaarImageClient } from "@/utils/aadhaarDecoder";



export default function ITR1Filing() {
  // states to manage document status and selection
  const [selectedDocs, setSelectedDocs] = useState({
    ais: true,
    tis: true,
    form26as: true,
    prefill: true,
    panCard: true,
    aadhaarCard: true,
  });

  // stores parsed JSON structures bubbled up from cards
  const [uploadedFiles, setUploadedFiles] = useState({
    ais: null,
    tis: null,
    form26as: null,
    prefill: null,
    panCard: null,
    aadhaarCard: null,
  });

  // Form states initialized from imported defaults
  const [profile, setProfile] = useState(INITIAL_PROFILE);
  const [address, setAddress] = useState(INITIAL_ADDRESS);
  const [bank, setBank] = useState(INITIAL_BANK);
  const [verification, setVerification] = useState(INITIAL_VERIFICATION);

  const updateStates = (nextFiles) => {
    const merged = mergeTaxpayerData(nextFiles.prefill, nextFiles.panCard, nextFiles.aadhaarCard);
    setProfile(merged.profile);
    setAddress(merged.address);
    setBank(merged.bank);
    setVerification(merged.verification);
  };

  // handle prefill file changes
  const handlePrefillFileChange = (data) => {
    setUploadedFiles((prev) => {
      const next = { ...prev, prefill: data };
      updateStates(next);
      return next;
    });
  };

  const handlePanCardChange = (data) => {
    setUploadedFiles((prev) => {
      const next = { ...prev, panCard: data };
      updateStates(next);
      return next;
    });
  };

  const handleAadhaarCardChange = (data) => {
    setUploadedFiles((prev) => {
      const next = { ...prev, aadhaarCard: data };
      updateStates(next);
      return next;
    });
  };

  const [generatedJson, setGeneratedJson] = useState(null);

  // toggle document selection
  const toggleDocSelection = (doc) => {
    setSelectedDocs((prev) => ({
      ...prev,
      [doc]: !prev[doc],
    }));
  };

  const handleParseFile = (file, docType) => parseTaxFile(file, profile.pan, profile.dob, docType);

  // handle data bubble-up from cards
  const handleFileChange = (docType, data) => {
    setUploadedFiles((prev) => ({
      ...prev,
      [docType]: data,
    }));
  };

  // handles JSON generation using uploaded files and form states
  const handleGenerateJson = () => {
    const dataPayload = {
      taxpayerInfo: {
        name: profile.name,
        pan: profile.pan,
        dob: profile.dob,
        employerCategory: profile.employerCategory,
        aadhaarCardNo: profile.aadhaarCardNo,
        email: profile.email,
        phone: profile.phone,
        section80C: profile.section80C,
        section80D: profile.section80D,
        section80TTA: profile.section80TTA
      },
      addressInfo: {
        residenceNo: address.residenceNo,
        residenceName: address.residenceName,
        roadOrStreet: address.roadOrStreet,
        localityOrArea: address.localityOrArea,
        cityOrTownOrDistrict: address.cityOrTownOrDistrict,
        stateCode: address.stateCode,
        pinCode: address.pinCode
      },
      bankInfo: {
        ifscCode: bank.ifscCode,
        bankName: bank.bankName,
        bankAccountNo: bank.bankAccountNo,
        accountType: bank.accountType,
        useForRefund: bank.useForRefund
      },
      verificationInfo: {
        fatherName: verification.fatherName,
        capacity: verification.capacity,
        place: verification.place,
        optOutNewTaxRegime: verification.optOutNewTaxRegime
      },
      ais: selectedDocs.ais ? uploadedFiles.ais : null,
      tis: selectedDocs.tis ? uploadedFiles.tis : null,
      form26as: selectedDocs.form26as ? uploadedFiles.form26as : null,
    };

    const finalJson = generateItr1Json(dataPayload);
    setGeneratedJson(finalJson);
  };

  const handleDownloadJson = () => {
    downloadJson(generatedJson);
  };

  const isAnyDocumentLoaded = 
    (selectedDocs.ais && uploadedFiles.ais) ||
    (selectedDocs.tis && uploadedFiles.tis) ||
    (selectedDocs.form26as && uploadedFiles.form26as);

  return (
    <div className="grid lg:grid-cols-12 gap-8 items-start animate-fade-in-up">
      {/* Left column: Selection and Load controls */}
      <div className="lg:col-span-6 flex flex-col gap-6">
        
        {/* Card 1: Documents Upload */}
        <div className="glass-card rounded-2xl p-6 sm:p-8">
          <h2 className="text-lg font-bold text-white mb-5 flex items-center gap-2">
            <SparklesIcon className="w-5 h-5 text-indigo-400" /> 1. Import Source Documents
          </h2>

          <div className="flex flex-col gap-4">
            {/* Prefill JSON Card */}
            <DocumentUploadCard 
              id="prefill"
              title="Prefill Data"
              badgeText="Taxpayer Prefill"
              description="Upload prefill JSON (e.g. AADPB1956F-Prefill...) to automatically load taxpayer profile, address, bank, and verification."
              selected={selectedDocs.prefill}
              onToggle={() => toggleDocSelection("prefill")}
              onFileChange={handlePrefillFileChange}
            />

            {/* PAN Card Card */}
            <DocumentUploadCard 
              id="panCard"
              title="PAN Card"
              badgeText="Identity Extraction"
              description="Upload a photo or PDF of your PAN card to automatically extract PAN details."
              selected={selectedDocs.panCard}
              onToggle={() => toggleDocSelection("panCard")}
              onFileChange={handlePanCardChange}
              onParseFile={parsePanImageClient}
            />

            {/* Aadhaar Card Card */}
            <DocumentUploadCard 
              id="aadhaarCard"
              title="Aadhaar Card"
              badgeText="Identity &amp; Address Extraction"
              description="Upload a photo or PDF of your Aadhaar card to extract Aadhaar and address details."
              selected={selectedDocs.aadhaarCard}
              onToggle={() => toggleDocSelection("aadhaarCard")}
              onFileChange={handleAadhaarCardChange}
              onParseFile={parseAadhaarImageClient}
            />
            {/* AIS Card */}
            <DocumentUploadCard 
              id="ais"
              title="AIS"
              badgeText="Annual Information"
              description="Includes salary, dividend, mutual funds, interest details."
              selected={selectedDocs.ais}
              onToggle={() => toggleDocSelection("ais")}
              onFileChange={(data) => handleFileChange("ais", data)}
              onParseFile={(file) => handleParseFile(file, "ais")}
            />

            {/* TIS Card */}
            <DocumentUploadCard 
              id="tis"
              title="TIS"
              badgeText="Taxpayer Summary"
              description="Aggregated values of all transactions for simplified filing."
              selected={selectedDocs.tis}
              onToggle={() => toggleDocSelection("tis")}
              onFileChange={(data) => handleFileChange("tis", data)}
              onParseFile={(file) => handleParseFile(file, "tis")}
            />

            {/* Form 26AS Card */}
            <DocumentUploadCard 
              id="form26as"
              title="Form 26AS"
              badgeText="Tax Credit"
              description="Tax credit statement showing TDS deposited by employer/banks."
              selected={selectedDocs.form26as}
              onToggle={() => toggleDocSelection("form26as")}
              onFileChange={(data) => handleFileChange("form26as", data)}
              onParseFile={(file) => handleParseFile(file, "form26as")}
            />
          </div>
        </div>

        {/* Prefilled Information Display (Read-Only) */}
        <ITRPrefillDetails 
          profile={profile}
          address={address}
          bank={bank}
          verification={verification}
        />

        {/* Generate Action Button */}
        <button
          onClick={handleGenerateJson}
          disabled={!isAnyDocumentLoaded}
          className="w-full py-4 rounded-full bg-gradient-to-r from-indigo-500 to-emerald-500 text-white font-bold text-base shadow-lg hover:shadow-indigo-500/20 hover:-translate-y-0.5 active:translate-y-0 disabled:opacity-50 disabled:pointer-events-none transition-all duration-200 cursor-pointer"
        >
          Generate Income Tax JSON
        </button>
      </div>

      {/* Right column: Reusable JSON Output Preview */}
      <div className="lg:col-span-6">
        <OutputJsonViewer 
          data={generatedJson} 
          onDownload={handleDownloadJson} 
          uploadedFiles={uploadedFiles}
        />
      </div>
    </div>
  );
}
