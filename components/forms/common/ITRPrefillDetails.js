"use client";

export default function ITRPrefillDetails({
  profile,
  address,
  bank,
  verification
}) {
  return (
    <div className="glass-card rounded-2xl p-6 sm:p-8 flex flex-col gap-6">
      <div>
        <h2 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
          <svg className="w-5 h-5 text-indigo-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
            <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2" />
            <circle cx="12" cy="7" r="4" />
          </svg>
          2. Prefilled Taxpayer Information
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
          <div className="bg-surface/30 p-3 rounded-xl border border-border/40">
            <span className="block text-[10px] uppercase tracking-wider text-text-muted font-bold mb-1">Full Name</span>
            <span className="text-white font-medium">{profile.name || <span className="text-text-muted italic">Not Loaded (Upload Prefill JSON)</span>}</span>
          </div>
          <div className="bg-surface/30 p-3 rounded-xl border border-border/40">
            <span className="block text-[10px] uppercase tracking-wider text-text-muted font-bold mb-1">PAN Card</span>
            <span className="text-white font-medium">{profile.pan || <span className="text-text-muted italic">Not Loaded</span>}</span>
          </div>
          <div className="bg-surface/30 p-3 rounded-xl border border-border/40">
            <span className="block text-[10px] uppercase tracking-wider text-text-muted font-bold mb-1">Date of Birth</span>
            <span className="text-white font-medium">{profile.dob || <span className="text-text-muted italic">Not Loaded</span>}</span>
          </div>
          <div className="bg-surface/30 p-3 rounded-xl border border-border/40">
            <span className="block text-[10px] uppercase tracking-wider text-text-muted font-bold mb-1">Aadhaar Card</span>
            <span className="text-white font-medium">{profile.aadhaarCardNo || <span className="text-text-muted italic">Not Loaded</span>}</span>
          </div>
          <div className="bg-surface/30 p-3 rounded-xl border border-border/40">
            <span className="block text-[10px] uppercase tracking-wider text-text-muted font-bold mb-1">Employer Category</span>
            <span className="text-white font-medium">{profile.employerCategory || <span className="text-text-muted italic">Not Loaded</span>}</span>
          </div>
          <div className="bg-surface/30 p-3 rounded-xl border border-border/40">
            <span className="block text-[10px] uppercase tracking-wider text-text-muted font-bold mb-1">Contact Info</span>
            <span className="text-white font-medium">
              {profile.phone || profile.email ? (
                `${profile.phone || ""} ${profile.phone && profile.email ? "/" : ""} ${profile.email || ""}`
              ) : (
                <span className="text-text-muted italic">Not Loaded</span>
              )}
            </span>
          </div>
        </div>
      </div>

      <div className="border-t border-border/40"></div>

      <div>
        <h2 className="text-sm font-bold text-white mb-3 flex items-center gap-2">
          <svg className="w-4 h-4 text-indigo-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
            <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" />
            <circle cx="12" cy="10" r="3" />
          </svg>
          Address
        </h2>
        <div className="bg-surface/30 p-4 rounded-xl border border-border/40 text-xs text-white leading-relaxed">
          {address.residenceNo || address.roadOrStreet || address.localityOrArea ? (
            <>
              {address.residenceNo && <div>{address.residenceNo}</div>}
              {address.residenceName && <div>{address.residenceName}</div>}
              {address.roadOrStreet && <div>{address.roadOrStreet}</div>}
              {address.localityOrArea && <div>{address.localityOrArea}</div>}
              {address.cityOrTownOrDistrict && <div>{address.cityOrTownOrDistrict}</div>}
              <div>State Code: {address.stateCode} | Pin Code: {address.pinCode}</div>
            </>
          ) : (
            <span className="text-text-muted italic">Not Loaded (Upload Prefill JSON)</span>
          )}
        </div>
      </div>

      <div className="border-t border-border/40"></div>

      <div>
        <h2 className="text-sm font-bold text-white mb-3 flex items-center gap-2">
          <svg className="w-4 h-4 text-indigo-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
            <rect x="2" y="5" width="20" height="14" rx="2" />
            <line x1="2" y1="10" x2="22" y2="10" />
          </svg>
          Bank &amp; Verification
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
          <div className="bg-surface/30 p-3 rounded-xl border border-border/40">
            <span className="block text-[10px] uppercase tracking-wider text-text-muted font-bold mb-1">Bank Name</span>
            <span className="text-white font-medium">{bank.bankName || <span className="text-text-muted italic">Not Loaded</span>}</span>
          </div>
          <div className="bg-surface/30 p-3 rounded-xl border border-border/40">
            <span className="block text-[10px] uppercase tracking-wider text-text-muted font-bold mb-1">Account &amp; IFSC</span>
            <span className="text-white font-medium">
              {bank.bankAccountNo || bank.ifscCode ? (
                `${bank.bankAccountNo || ""} (${bank.accountType}) | ${bank.ifscCode || ""}`
              ) : (
                <span className="text-text-muted italic">Not Loaded</span>
              )}
            </span>
          </div>
          <div className="bg-surface/30 p-3 rounded-xl border border-border/40">
            <span className="block text-[10px] uppercase tracking-wider text-text-muted font-bold mb-1">Father&apos;s Name</span>
            <span className="text-white font-medium">{verification.fatherName || <span className="text-text-muted italic">Not Loaded</span>}</span>
          </div>
          <div className="bg-surface/30 p-3 rounded-xl border border-border/40">
            <span className="block text-[10px] uppercase tracking-wider text-text-muted font-bold mb-1">Verification Details</span>
            <span className="text-white font-medium">
              {verification.capacity || verification.place ? (
                `Capacity: ${verification.capacity === "S" ? "Self" : "Representative"} | Place: ${verification.place || ""}`
              ) : (
                <span className="text-text-muted italic">Not Loaded</span>
              )}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
