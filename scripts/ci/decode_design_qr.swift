import Foundation
import Vision
import AppKit
guard CommandLine.arguments.count == 2 else {
    FileHandle.standardError.write(Data("usage: swift decode_design_qr.swift <exported-image>\n".utf8))
    exit(2)
}
let url = URL(fileURLWithPath: CommandLine.arguments[1])
let request = VNDetectBarcodesRequest()
request.symbologies = [.qr]
try VNImageRequestHandler(url: url, options: [:]).perform([request])
let results = (request.results ?? []).map { ["payload": $0.payloadStringValue ?? "", "confidence": String($0.confidence)] }
let data = try JSONSerialization.data(withJSONObject: results, options: [.prettyPrinted])
print(String(data: data, encoding: .utf8)!)
